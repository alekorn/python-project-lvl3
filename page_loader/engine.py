import argparse
import requests
import re
import os
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
    parse_url = urlparse(url)
    file_name = normalize_url(url) + '.html'
    dir_name = output + '/' + normalize_url(url) + '_files'
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    file_save(os.path.join(output, file_name), text, 'w')
    attr_texts = soup_attr_find(soup, TAGS_ATTRS)
    print(*attr_texts) # debug
    os.mkdir(dir_name)
    for attr_text in attr_texts:
        parse_attr = urlparse(attr_text)
        if parse_attr.scheme:
            data = requests.get(attr_text)
        else:
            data = requests.get(parse_url.scheme + '://' + parse_url.netloc + attr_text)
        file_save(dir_name + '/' + normalize_url(attr_text), data.content, 'wb') # change 3 arg


def soup_attr_find(soup, tag_attr_dict):
    result_list = []
    for key, value in tag_attr_dict.items():
        for link in soup.find_all(key):
            if link.get(value):
                result_list.append(link.get(value))
    return result_list


def file_save(file_path, data, data_type):
    with open(file_path, data_type) as output_file:
        output_file.write(data)


# def soup_attr_finder_old(soup, tag, attr):
#     result_list = []
#     for link in soup.find_all(tag):
#         if link.get(attr):
#             result_list.append(link.get(attr))
#     return result_list


def normalize_url(url):
    parsed_url = urlparse(url)
    if '.' in parsed_url.path:
        path, ext = parsed_url.path.rsplit('.', 1)
        ext = '.' + ext
    else:
        path = parsed_url.path
        ext = ''
    normalized_path = re.sub(r'[^a-zA-Z0-9]', '-', parsed_url.netloc + path)
    return normalized_path.strip('-') + ext
