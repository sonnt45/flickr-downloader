import os
import requests
import flickrapi
from bs4 import *
from vendor import mimetypes


api_key = ('c6a2c45591d4973ff525042472446ca2')
api_secret = ('202ffe6f387ce29b')
download_directory = ('download')
log_directory = ('log')
size_paths = (['o', 'k', 'h', 'l', 'c', 'z', 'm', 'w', 'n', 's', 't', 'q', 'sq'])


def main():

    user_id = input('Enter user ID: ')

    if user_id:
        create_directory(download_directory)
        create_directory(log_directory)
        download_photos_by_user_id(user_id)
    else:
        print('Aborted')


def create_directory(directory, reuse = True):

    if os.path.exists(directory):
        if not reuse:
            return create_directory(directory + '_')
    else:
        os.mkdir(directory)

    return directory


def open_directory(directory):

    if os.path.exists(directory):
        os.startfile(os.path.realpath(directory))


def download_photos_by_user_id(user_id, ):

    photo_ids = get_photo_ids_by_user_id(user_id)
    total_count = len(photo_ids)

    if total_count == 0:
        print('There is no photo to download')
    else:
        downloaded_ids = read_log(user_id)
        downloaded_count = 0
        file_path = create_directory(f'{download_directory}/{user_id}')

        for photo_id in photo_ids:
            id = f'{user_id}/{photo_id}'

            if downloaded_ids != None and photo_id in downloaded_ids:
                print(f'Ignored {id}')
                downloaded_count += 1
                print(f'Downloaded {downloaded_count}/{total_count}')
            else:
                print(f'Downloading {id}')

                if download_photo(id, f'{file_path}/{photo_id}'):
                    write_log(user_id, photo_id)
                    downloaded_count += 1
                    print(f'Downloaded {downloaded_count}/{total_count}')
                else:
                    print('Failed')

        if downloaded_count > 0:
            open_directory(file_path)


def get_photo_ids_by_user_id(user_id):

    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    photo_ids = []

    try:
        for photo in flickr.walk(user_id=user_id):
            photo_ids.append(photo.get('id'))
    except Exception as exception:
        print(exception)

    return photo_ids


def download_photo(photo_path, file_path):

    for size_path in size_paths:
        try:
            image = requests.get(
                BeautifulSoup(requests.get(f'https://www.flickr.com/photos/{photo_path}/sizes/{size_path}').text, 'html.parser')
                .find('div', attrs = {'id':'allsizes-photo'})
                .find('img')['src'])

            with open(file_path + mimetypes.guess_extension(image.headers['content-type']), 'wb+') as file:
                file.write(image.content)

            return True
        except Exception as exception:
            print(exception)

    return False


def read_log(user_id):

    path = f'{log_directory}/{user_id}'

    if os.path.exists(path):
        with open(path, 'r') as file:
            return file.read()


def write_log(user_id, last_photo_id):

    path = f'{log_directory}/{user_id}'

    with open(path, 'a' if os.path.exists(path) else 'w') as file:
        if last_photo_id:
            file.write(f'{last_photo_id}\n')


main()
