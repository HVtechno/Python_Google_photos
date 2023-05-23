import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def authenticate_google_photos_api():
    # Set up the OAuth 2.0 flow for authentication
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', ['https://www.googleapis.com/auth/photoslibrary.readonly'])
    credentials = flow.run_local_server(port=0)

    return credentials


def download_media(media_item):
    base_dir = 'downloaded_media'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    filename = os.path.join(base_dir, media_item['filename'])
    url = media_item['baseUrl'] + "=d"

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        print(f"Unable to download {media_item['filename']}. Error: {response.status_code}")


def download_all_media(service):
    media_items = []

    page_token = ""
    while page_token is not None:
        response = service.mediaItems().list(pageSize=100, pageToken=page_token).execute()

        media_items.extend(response.get('mediaItems', []))
        page_token = response.get('nextPageToken', None)

    print(f"Total media items: {len(media_items)}")

    for media_item in media_items:
        download_media(media_item)


def main():
    credentials = authenticate_google_photos_api()
    service = build('photoslibrary', 'v1', credentials=credentials)

    download_all_media(service)


if __name__ == '__main__':
    main()
