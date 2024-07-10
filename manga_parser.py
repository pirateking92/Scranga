import requests
import json
import os
from manga_searcher import get_first_manga_id_and_chapter


def download_latest_manga_chapter(chapter_id, manga_name):
    # url is for the chapter of haikyuu that i have most recently read
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    res = requests.get(url)

    if res.status_code != 200:
        print("Failed to access JSON data")
    else:
        json_data = res.json()

        # extracting the fields needed for the url
        base_url = json_data['baseUrl']
        chapter_hash = json_data['chapter']['hash']
        image_data = json_data['chapter']['data']

        # defining the path to manga_scrapes in icloud drive
        folder_path = os.path.expanduser(
            f'/Users/mattdoyle/Library/Mobile Documents/com~apple~CloudDocs/manga_scrapes/{manga_name}'
        )
        os.makedirs(folder_path, exist_ok=True)

        # constructing the urls and downloading the images
        for image_name in image_data:
            image_url = f"{base_url}/data/{chapter_hash}/{image_name}"
            image_response = requests.get(image_url)
            print(image_url)

            if image_response.status_code == 200:
                image_path = os.path.join(folder_path, image_name)
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                print(f"Downloaded: {image_name}")
            else:
                print(f"Failed to download: {image_name}")


# Get manga info once
manga_id, chapter_id, manga_name = get_first_manga_id_and_chapter()

# Call the download function with the obtained info
if chapter_id and manga_name:
    download_latest_manga_chapter(chapter_id, manga_name)
else:
    print("Failed to get manga information.")

# so that the json can be read easier if need be
# json_data = res.json()
# readable_json = json.dumps(json_data, indent=4)
# print(readable_json)
