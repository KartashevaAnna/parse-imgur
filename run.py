import csv
import json
import os
import string

import requests

from bearer_token import CLIENT_ID
from constants import (
    ALBUMS_DIRECTORY,
    HEADERS,
    IMAGES_DIRECTORY,
    RESULTS_DIRECTORY,
    USER_TO_PARSE,
)
from schemas.schema import Album, Image


def create_directories() -> None:
    directories = [
        f"{ALBUMS_DIRECTORY}/{USER_TO_PARSE}",
        f"{IMAGES_DIRECTORY}/{USER_TO_PARSE}",
        f"{RESULTS_DIRECTORY}/{USER_TO_PARSE}",
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def get_list_of_album_links(page_number) -> int | int:
    url = f"https://api.imgur.com/post/v1/accounts/{USER_TO_PARSE}/submissions?client_id={CLIENT_ID}&include=media&page={page_number}&sort=-gallery_id"

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        albums = response.json()
        if not albums:
            return "stop iteration"
        albums = [Album(id=x["id"], title=x["title"]) for x in albums]
        albums_links_json = [x.model_dump_json() for x in albums]
        #  save album list to json file so that we do not repeat the requests for any further manipulations with data
        with open(
            f"all_albums/{USER_TO_PARSE}/album_links_{USER_TO_PARSE}_{page_number}.json",
            "w+",
            encoding="utf-8",
        ) as jsonfile:
            jsonfile.write(json.dumps(albums_links_json, indent=4))

    else:
        with open(
            f"all_albums/{USER_TO_PARSE}/album_errors_{USER_TO_PARSE}_{page_number}.txt",
            "a+",
            encoding="utf-8",
        ) as file:
            file.write(response.text)


def get_album_contents(
    albums_links: list[Album.link],
) -> list[str]:
    albums_with_images = {}
    for url in albums_links:
        url = json.loads(url)
        response = requests.get(url["link"], headers=HEADERS)
        if response.status_code == 200:
            images = response.json()["data"]["images"]
            albums_with_images[url["id"]] = [
                Image(link=x["link"]).link for x in images
            ]
        else:
            with open(
                f"{RESULTS_DIRECTORY}/{USER_TO_PARSE}/errors.txt", "a+"
            ) as file:
                file.write(response.text)
    return albums_with_images


def save_all_albums():
    """Save albums contents to json file.

    It is done so that we do not repeat the requests
    for any further manipulations with data."""

    all_albums = os.listdir(
        f"/home/anna/Documents/Dev/parse-imgur/all_albums/{USER_TO_PARSE}"
    )
    for album in all_albums:
        with open(f"{ALBUMS_DIRECTORY}/{USER_TO_PARSE}/{album}", "r") as file:
            data = json.load(file)

            images_links = get_album_contents(data)
            with open(
                f"{IMAGES_DIRECTORY}/{USER_TO_PARSE}/{album}_images_links.json",
                "w",
                encoding="utf-8",
            ) as jsonf:
                jsonf.write(json.dumps(images_links, indent=4))


def count_all_albums() -> int:
    all_files = os.listdir(f"{ALBUMS_DIRECTORY}{USER_TO_PARSE}")
    all_albums = 0
    for album in all_files:
        with open(
            f"{ALBUMS_DIRECTORY}{USER_TO_PARSE}/{album}",
            "r",
            encoding="utf-8",
        ) as file:
            albums = json.load(file)
            all_albums += len(albums)
    return all_albums


def get_human_readable_link(title: str, id: str) -> str:
    link = title.lower()
    for character in link:
        if character in string.punctuation:
            link = link.replace(character, "")
        link = link.replace("the", "")
        link = "-".join(link.split())
    return f"https://imgur.com/gallery/{link}-{id}"


def save_human_readable_links_to_albums():
    """Create human readable links to albums.

    Save them to a new json file."""
    all_albums = os.listdir(
        # f"/home/anna/Documents/Dev/parse-imgur/all_albums/{USER_TO_PARSE}"
        f"{ALBUMS_DIRECTORY}/{USER_TO_PARSE}"
    )
    final_hh_links = {}
    for album in all_albums:
        with open(f"{ALBUMS_DIRECTORY}/{USER_TO_PARSE}/{album}", "r") as file:
            data = json.load(file)
            for entry in data:
                entry_data = json.loads(entry)
                entry_data["readable_link"] = get_human_readable_link(
                    title=entry_data["title"], id=entry_data["id"]
                )
                final_hh_links[entry_data["id"]] = entry_data
    with open(
        f"{RESULTS_DIRECTORY}{USER_TO_PARSE}/all_albums_with_human_links.json",
        "w+",
    ) as file:
        file.write(json.dumps(final_hh_links, indent=4))


def get_all_links_to_photos() -> dict:
    all_links = os.listdir(IMAGES_DIRECTORY)
    all_data = {}
    for entry in all_links:
        with open(
            f"{IMAGES_DIRECTORY}/{entry}",
            "r",
            encoding="utf-8",
        ) as file:
            my_links = json.load(file)
            for key in my_links.keys():
                all_data[key] = my_links[key]


def save_final_files():
    final_list = []
    with open(
        f"{RESULTS_DIRECTORY}{USER_TO_PARSE}/all_albums_with_human_links.json",
        "r",
    ) as linksfile:
        human_links = json.load(linksfile)
        final_list.extend(
            human_links[key]["readable_link"] for key in human_links.keys()
        )
    with open(
        f"{RESULTS_DIRECTORY}{USER_TO_PARSE}/all_albums_with_human_links.csv",
        "a+",
    ) as finalfile:
        csvwriter = csv.writer(finalfile)
        csvwriter.writerows((item,) for item in final_list)


def save_filtered_values(filter_str: str):
    filtered_links = []
    with open(
        f"{RESULTS_DIRECTORY}{USER_TO_PARSE}/all_albums_with_human_links.csv",
    ) as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            if filter_str in row[0]:
                filtered_links.extend(row)
    with open(
        f"{RESULTS_DIRECTORY}{USER_TO_PARSE}/all_albums_with_human_links_filtered.csv",
        "w+",
    ) as finalfile:
        csvwriter = csv.writer(finalfile)
        csvwriter.writerows((item,) for item in filtered_links)


def main():
    create_directories()
    for i in range(1, 35):
        res = get_list_of_album_links(i)
        if res == "stop iteration":
            break
    print(count_all_albums())
    save_human_readable_links_to_albums()
    save_final_files()
    save_filtered_values("scifishenanigansepicgeekery")


if __name__ == "__main__":
    main()
