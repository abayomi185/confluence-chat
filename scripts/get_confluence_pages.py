import argparse

from dotenv import load_dotenv

load_dotenv()

import json
import os

from atlassian import Confluence
from bs4 import BeautifulSoup

DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../data"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--download", action="store_true", help="Download documents from Confluence"
)
args = parser.parse_args()

confluence = Confluence(
    url=os.environ["ATLASSIAN_URL"],
    username=os.environ["ATLASSIAN_USER"],
    password=os.environ["ATLASSIAN_TOKEN"],
    cloud=True,
)


def get_all_pages_from_space_and_write_to_json(space_key: str):
    all_pages = confluence.get_all_pages_from_space(space_key, limit=1000)
    with open(f"{DATA_DIR}/all_pages.json", "w") as file:
        file.write(str(all_pages))


def get_plain_text_from_page_id_and_write_to_file(page_id: int):
    print(f"Getting page {page_id}")
    page_details = confluence.get_page_by_id(
        page_id, "space,body.view,version,container"
    )
    soup = BeautifulSoup(page_details["body"]["view"]["value"], "html.parser")  # type: ignore
    plain_text = soup.get_text()
    with open(f"{DATA_DIR}/page_{page_id}.txt", "w") as file:
        file.write(page_details["title"] + "\n")  # type: ignore
        # Possibly add labels too
        file.write(plain_text)


if __name__ == "__main__":
    # To get all pages from a space
    if args.download:
        get_all_pages_from_space_and_write_to_json("SD")

    with open(f"{DATA_DIR}/all_pages.json", "r") as file:
        all_pages = json.load(file)

    for page in all_pages:
        get_plain_text_from_page_id_and_write_to_file(page["id"])
