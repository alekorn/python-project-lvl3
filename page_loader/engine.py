import argparse
import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader.logger import LOGGER
from progress.bar import IncrementalBar

TAGS_ATTRS = {'link': 'href', 'script': 'src', 'img': 'src'}


class KnownError(Exception):
    pass


def arg_parse(argv):
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('url', type=str, help='')
    parser.add_argument(
        '-l',
        '--log',
        help='',
        type=str,
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info'
    )
    parser.add_argument(
        '-o',
        '--output',
        help='',
        type=str,
        default='./'
    )
    args = parser.parse_args(argv)
    return args


def page_load(output, url):
    url = normalize_url(url)
    name = get_name(url)
    file_name = f'{name}.html'
    dir_name = f'{name}_files'
    file_path = os.path.join(output, file_name)
    dir_path = os.path.join(output, dir_name)
    page_text = get_html(url)
    create_dir(dir_path)
    content_list, data = get_data(page_text, TAGS_ATTRS, dir_name)
    save_page(file_path, data)
    save_content(content_list, dir_path, url)


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
                content_list.append(link[value])
                link[value] = os.path.join(dir_name, get_name(link[value]))
    LOGGER.info(f"change data in getted html")
    return content_list, str(soup)


def save_content(content_list, dir_path, url):
    with IncrementalBar('Processing', max=len(content_list)) as bar:
        for attr_text in content_list:
            parse_attr = urlparse(attr_text)
            if parse_attr.scheme:
                data = requests.get(attr_text)
            else:
                LOGGER.debug(os.path.join(url, attr_text))  # DEBUG
                LOGGER.debug(f'{url}')  # DEBUG
                LOGGER.debug(f'{attr_text}')  # DEBUG
                data = requests.get(urljoin(url, attr_text))  # TODO add test
            file_path = os.path.join(dir_path, get_name(attr_text))
            save_file(file_path, data.content)
            bar.next()


def save_page(file_path, data):
    try:
        with open(file_path, 'w') as output_file:
            output_file.write(data)
    except OSError as error:
        LOGGER.error(error)
        raise KnownError(error)  # TODO IOError???
    else:
        LOGGER.info(f"page saved {file_path}")


def save_file(file_path, data):
    try:
        with open(file_path, 'wb') as output_file:
            output_file.write(data)
    except OSError as error:
        LOGGER.error(error)
        raise KnownError(error)
    else:
        LOGGER.info(f"file saved {file_path}")


def create_dir(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError as error:
        LOGGER.error(error)
        raise KnownError(error)
    else:
        LOGGER.warning(f"directory created {dir_path}")


def normalize_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        LOGGER.warning(f"{url} has no schema, url changed to http://{url}")
        url = f'http://{url}'
    return url
