import requests
from bs4 import BeautifulSoup
from page_loader.logger import LOGGER, KnownError
from urllib.parse import urlparse
import os
import re


def get_name(url):
    parsed_url = urlparse(url)
    file_name, ext = os.path.splitext(parsed_url.path)
    normalized_path = re.sub(
            r'[^a-zA-Z0-9]',
            '-', parsed_url.netloc + file_name
            )
    return normalized_path.strip('-') + ext


def get_html(url):
    try:
        response = requests.get(url)
    except requests.RequestException as error:
        LOGGER.error(error)
        raise KnownError(error)
    try:
        response.raise_for_status()
    except requests.RequestException as error:
        LOGGER.error(error)
        raise KnownError(error)
    else:
        LOGGER.info(f"get html {url}")
        response = requests.get(url)
        return response.text


def get_data(page_text, tag_attr_dict, dir_name):
    soup = BeautifulSoup(page_text, 'html.parser')
    content_list = []
    for key, value in tag_attr_dict.items():
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
