from argparse import ArgumentParser
import urllib.request
import requests
import json
import django
import os
import sys

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_api.settings')
django.setup()

from api.serializers import PhotoSerializer

PHOTOS_DIR = r'C:/Users/Marcel/Programowanie/Zadania_rekrutacyjne/Friendly_Solutions/rest_api/photos/'
JSON_FILEPATH = r'C:\Users\Marcel\Programowanie\Zadania_rekrutacyjne\Friendly_Solutions\rest_api\photos.json'


def handle_arguments():
    parser = ArgumentParser(
        prog='Photos REST API',
        description='Importing photos from external resources')
    parser.add_argument('--source',
                        choices=['api', 'json'],
                        help='Source of the photos data')
    return parser.parse_args()


def save_photo(url, filepath):
    res = requests.get(url,
                       stream=True,
                       headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                                              '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                                }
                       )
    if res.status_code == 200:
        with open(filepath, 'wb') as handler:
            handler.write(res.content)


def create_photos(photos):
    photos_created = 0
    for photo in photos:
        # not working now because I cannot download and save the image (403 always)
        # filepath = os.path.abspath(
        #     os.path.join(os.sep, PHOTOS_DIR, f'{photo["title"].replace(" ", "_")}.png'))\
        #     .replace('\\', '/')
        mock_filepath = os.path.abspath(
            os.path.join(os.sep, PHOTOS_DIR, 'mock_photo.jpg')).replace('\\', '/')
        # save_photo(photo['url'], filepath)

        data = {
            'url': mock_filepath,
            'title': photo['title'],
            'album_id': photo['albumId'],
        }

        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            photos_created += 1
        else:
            print(f'ERROR: Problem occurred when saving "{photo["title"]}" photo.\n'
                  f'{serializer.errors}')

    print(f'Successfully created {photos_created} photos.')


def import_photos_from_api():
    with urllib.request.urlopen('https://jsonplaceholder.typicode.com/photos') as url:
        photos = json.load(url)
        create_photos(photos)


def import_photos_from_json():
    with open(JSON_FILEPATH, 'r') as file:
        photos = json.load(file)
        create_photos(photos)


def import_photos():
    args = handle_arguments()

    if args.source == 'api':
        import_photos_from_api()
    elif args.source == 'json':
        import_photos_from_json()


if __name__ == '__main__':
    import_photos()
