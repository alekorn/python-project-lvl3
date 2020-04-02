import argparse
import requests
import re
import os
import copy
from bs4 import BeautifulSoup
from urllib.parse import urlparse

TAGS_ATTRS = {'link': 'href', 'script': 'src', 'img': 'src'}


def arg_parse(argv):
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('url', type=str, help='')
    parser.add_argument(
        '-o',
        '--output',
        help='',
        type=str,
    )
    args = parser.parse_args(argv)
    return args


def page_load(output, url):
    file_name = f'{normalize_url(url)}.html'
    dir_name = f'{normalize_url(url)}_files'
    dir_path = f'{output}/{dir_name}'
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    attr_texts, new_soup = soup_attr_find(soup, TAGS_ATTRS, dir_name)
    file_save(os.path.join(output, file_name), str(new_soup), 'w')
    os.mkdir(dir_path)
    for attr_text in attr_texts:
        parse_attr = urlparse(attr_text)
        if parse_attr.scheme:
            data = requests.get(attr_text)
        else:
            data = requests.get(f'{url}/{attr_text}')
        file_save(f'{dir_path}/{normalize_url(attr_text)}', data.content, 'wb')


def soup_attr_find(soup, tag_attr_dict, dir_name):
    new_soup = copy.copy(soup)
    result_list = []
    for key, value in tag_attr_dict.items():
        for link in new_soup.find_all(key):
            if value in link.attrs:
                result_list.append(link[value])
                link[value] = dir_name + '/' + normalize_url(link[value])
    return result_list, new_soup


def file_save(file_path, data, data_type):
    with open(file_path, data_type) as output_file:
        output_file.write(data)


def normalize_url(url):
    parsed_url = urlparse(url)
    file_name, ext = os.path.splitext(parsed_url.path)
    normalized_path = re.sub(
            r'[^a-zA-Z0-9]',
            '-', parsed_url.netloc + file_name
            )
    return normalized_path.strip('-') + ext
