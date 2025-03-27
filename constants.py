from bearer_token import TOKEN

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}
USER_TO_PARSE = "lydecker17"

ALBUMS_DIRECTORY = "all_albums/"
IMAGES_DIRECTORY = "images_links/"
RESULTS_DIRECTORY = "results/"
