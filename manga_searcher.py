import requests
import json


def get_first_manga_id_and_chapter():
    base_url = "https://api.mangadex.org"

    manga_name = input("Enter the name of the manga you are looking for: ")

    # check if response is successful
    r = requests.get(f"{base_url}/manga", params={"title": manga_name})
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return None, None, manga_name
    else:
        data = r.json().get("data", [])
        if not data:
            print("No manga found with that name.")
            return None, None, manga_name
        else:
            first_manga_id = data[0]['id']

            # this code then gets the full details and prints them to the terminal
            manga_details_response = requests.get(
                f"{base_url}/manga/{first_manga_id}")
            if manga_details_response.status_code == 200:
                manga_details = manga_details_response.json()
                manga_title = manga_details['data']['attributes']['title'][
                    'en']
                latest_chapter_id = manga_details['data']['attributes'][
                    'latestUploadedChapter']

                print(f"Manga title: {manga_title}")
                print(f"First manga ID: {first_manga_id}")
                print(f"Latest chapter ID: {latest_chapter_id}")
                print(json.dumps(manga_details, indent=4))

                return first_manga_id, latest_chapter_id, manga_name
            else:
                print(
                    f"Error fetching manga details: {manga_details_response.status_code}"
                )
                return first_manga_id, None, manga_name


# get_first_manga_id_and_chapter()
