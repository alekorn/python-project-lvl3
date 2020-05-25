import os
import re
import logging
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.logging import KnownError


def get_name(url):
    parsed_url = urlparse(url)
    file_name, ext = os.path.splitext(parsed_url.path)
    normalized_path = re.sub(
            r'[^a-zA-Z0-9]',
            '-', parsed_url.netloc + file_name
            )
    return normalized_path.strip('-') + ext


def download(url):
    logger = logging.getLogger()
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as error:
        logger.error(error)
        raise KnownError(error)
    else:
        logger.info(f"get html {url}")


def change_attrs(page_text, dir_name):
    logger = logging.getLogger()
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
                logger.debug(
                        f"attribute {key}='{old_value}' "
                        f"changed to {key}='{new_value}'"
                        )
    logger.info(f"data in the received HTML is changed")
    return content_list, str(soup)


def normalize_url(url):
    logger = logging.getLogger()
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        logger.warning(f"{url} has no schema, url changed to http://{url}")
        url = f'http://{url}'
    return url
