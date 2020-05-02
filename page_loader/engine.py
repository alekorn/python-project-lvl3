import argparse
import os
from urllib.parse import urlparse

from page_loader.getters import get_data, get_html, get_name
from page_loader.logger import LOGGER
from page_loader.savers import create_dir, save_content, save_page


def arg_parse():
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
    args = parser.parse_args()
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
    content_list, data = get_data(page_text, dir_name)
    save_page(file_path, data)
    save_content(content_list, dir_path, url)


def normalize_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        LOGGER.warning(f"{url} has no schema, url changed to http://{url}")
        url = f'http://{url}'
    return url
