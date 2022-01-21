import os
import requests
import flickrapi
from bs4 import *
from vendor import mimetypes


api_key = ('c6a2c45591d4973ff525042472446ca2')
api_secret = ('202ffe6f387ce29b')
download_directory = ('download')
size_paths = (['o', 'k', 'h', 'l', 'c', 'z', 'm', 'w', 'n', 's', 't', 'q', 'sq'])


def main():

    user_id = input('Enter user ID: ')

    if user_id:
        create_super_directory()
        download_photos_by_user_id(user_id)
    else:
        print('Aborted')


def create_super_directory():

    try:
        os.mkdir(download_directory)
    except:
        pass


def create_sub_directory(directory):

    try:
        os.mkdir(directory)

        return directory
    except:
        return create_sub_directory(directory + '_')


def open_directory(directory):

    try:
        os.startfile(os.path.realpath(directory))
    except:
        print(f'Cannot open directory: {os.path.realpath(directory)}')


def download_photos_by_user_id(user_id):

    photo_ids = get_photo_ids_by_user_id(user_id)
    total_count = len(photo_ids)

    if total_count == 0:
        print('There is no photo to download')
    else:
        directory = create_sub_directory(f'{download_directory}/{user_id}')
        downloaded_count = 0

        for photo_id in photo_ids:
            id = f'{user_id}/{photo_id}'
            print(f'Downloading {id}')

            if download_photo(id, f'{directory}/{photo_id}'):
                downloaded_count += 1
                print(f'Downloaded {downloaded_count}/{total_count}')
            else:
                print('Failed')

        if downloaded_count > 0:
            open_directory(directory)


def get_photo_ids_by_user_id(user_id):

    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    photo_ids = []

    try:
        for photo in flickr.walk(user_id=user_id):
            photo_ids.append(photo.get('id'))
    except Exception as exception:
        print(exception)

    return photo_ids


def download_photo(photo_path, file_name):

    for size_path in size_paths:
        try:
            image = requests.get(
                BeautifulSoup(requests.get(f'https://www.flickr.com/photos/{photo_path}/sizes/{size_path}').text, 'html.parser')
                .find('div', attrs = {'id':'allsizes-photo'})
                .find('img')['src'])

            with open(file_name + mimetypes.guess_extension(image.headers['content-type']), 'wb+') as file:
                file.write(image.content)

            return True
        except Exception as exception:
            print(exception)

    return False


main()
