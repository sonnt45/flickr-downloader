# Flickr Downloader

This tiny Python tool can download all public photos of a user, even though they're disabled.

## Prerequisite

We need Python [Requests](https://pypi.org/project/requests) to scrape, [BeautifulSoup](https://pypi.org/project/bs4) to download and [FlickrAPI](https://pypi.org/project/flickrapi) to get photo IDs.

```bash
pip install requests
pip install html5lib
pip install bs4
pip install flickrapi
```

## Usage

There is only one feature, just run then enter the user ID:

```bash
python .\downloader.py
```

You can get the user ID from profile URLs, example `12345678N00` from:

- `https://www.flickr.com/people/12345678N00/...`
- `https://www.flickr.com/photos/12345678N00/...`

This tool will try to download the largest size of the photos. The downloaded photos are in `download` directory.

The log files in `log` directory contains downloaded IDs, which will be ignored in the next times you download.

## Known Issue

I'm using `Python 3.10.2` with `FlickrAPI 2.4.0`, so I got this error:

```bash
'xml.etree.ElementTree.Element' object has no attribute 'getchildren'
```

If you have the same error, try to find your `flickrapi/core.py`, in my case is:

```bash
%localappdata%\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\flickrapi\core.py
```

Edit line 690 from `photoset = rsp.getchildren()[0]` to `photoset = list(rsp)[0]`.

## References

- [GeeksforGeeks](https://www.geeksforgeeks.org/how-to-download-all-images-from-a-web-page-in-python)
- [FlickrAPI Document](https://stuvel.eu/flickrapi-doc/7-util.html)

## License

[MIT](https://choosealicense.com/licenses/mit)
