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
    USER_TO_PARSE,
)
from schemas.schema import Album, Image


def get_list_of_album_links(page_number) -> int | int:
    url = f"https://api.imgur.com/post/v1/accounts/{USER_TO_PARSE}/submissions?client_id={CLIENT_ID}&include=media&page={page_number}&sort=-gallery_id"

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        albums = response.json()
        albums = [Album(id=x["id"], title=x["title"]) for x in albums]
        albums_links_json = [x.model_dump_json() for x in albums]
        #  save album list to json file so that we do not repeat the requests for any further manipulations with data
        with open(
            f"all_albums/album_links_{page_number}.json", "w+", encoding="utf-8"
        ) as jsonfile:
            jsonfile.write(json.dumps(albums_links_json, indent=4))

    else:
        with open(
            f"all_albums/album_errors_{page_number}.txt", "w+", encoding="utf-8"
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
            print("#" * 100)
            print(response.text)
    return albums_with_images


def save_all_albums():
    """Save albums contents to json file.

    It is done so that we do not repeat the requests
    for any further manipulations with data."""

    all_albums = os.listdir("/home/anna/Documents/Dev/parse-imgur/all_albums")
    for album in all_albums:
        with open(f"{ALBUMS_DIRECTORY}/{album}", "r") as file:
            data = json.load(file)

            images_links = get_album_contents(data)
            with open(
                f"{IMAGES_DIRECTORY}/{album}_images_links.json",
                "w",
                encoding="utf-8",
            ) as jsonf:
                jsonf.write(json.dumps(images_links, indent=4))


def count_all_albums() -> int:
    all_files = os.listdir("/home/anna/Documents/Dev/parse-imgur/all_albums")
    all_albums = 0
    for _ in all_files:
        with open("images_links.json", "r", encoding="utf-8") as file:
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
    link = "https://imgur.com/gallery/" + link + "-" + id
    return link


def save_human_readable_links_to_albums():
    """Create human readable links to albums.

    Save them to a new json file."""
    all_albums = os.listdir("/home/anna/Documents/Dev/parse-imgur/all_albums")
    final_hh_links = {}
    for album in all_albums:
        with open(f"{ALBUMS_DIRECTORY}/{album}", "r") as file:
            data = json.load(file)
            for entry in data:
                entry_data = json.loads(entry)
                entry_data["readable_link"] = get_human_readable_link(
                    title=entry_data["title"], id=entry_data["id"]
                )
                final_hh_links[entry_data["id"]] = entry_data
    with open("all_albums_with_human_links.json", "w+") as file:
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


def main():
    for i in range(1, 67):
        get_list_of_album_links(i)
    print(count_all_albums())
    all_data = get_all_links_to_photos()
    with open("all_data.json", "w+") as file:
        file.write(json.dumps(all_data, indent=4))
    save_human_readable_links_to_albums()
    final_list = []
    with open("all_albums_with_human_links.json", "r") as linksfile:
        human_links = json.load(linksfile)
        for key in human_links.keys():
            final_list.append(human_links[key]["readable_link"])
            final_list.append("\n")
    with open("all_albums_with_human_links.csv", "a+") as finalfile:
        csvwriter = csv.writer(finalfile)
        csvwriter.writerows((item,) for item in final_list)
    with open("all_albums_with_human_links.text", "a+") as finalfile:
        for entry in final_list:
            finalfile.write(entry)


if __name__ == "__main__":
    main()
