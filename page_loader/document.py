import os
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.logger import LOGGER, KnownError


def get_name(url):
    parsed_url = urlparse(url)
    file_name, ext = os.path.splitext(parsed_url.path)
    normalized_path = re.sub(
            r'[^a-zA-Z0-9]',
            '-', parsed_url.netloc + file_name
            )
    return normalized_path.strip('-') + ext


def download(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        LOGGER.error(error)
        raise KnownError(error)
    else:
        LOGGER.info(f"get html {url}")


def change_attrs(page_text, dir_name):
    soup = BeautifulSoup(page_text, 'html.parser')
    tag_attrs = {'link': 'href', 'script': 'src', 'img': 'src'}
    content_list = []
    for key, value in tag_attrs.items():
        for link in soup.find_all(key):
            if value in link.attrs:
                old_value = link[value]
                content_list.append(link[value])
                link[value] = os.path.join(dir_name, get_name(link[value]))
                new_value = link[value]
                LOGGER.debug(
                        f"attribute {key}='{old_value}' "
                        f"changed to {key}='{new_value}'"
                        )
    LOGGER.info(f"data in the received HTML is changed")
    return content_list, str(soup)
