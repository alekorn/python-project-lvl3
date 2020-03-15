import argparse
import requests
import re
import os


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


def page_loader(output, url):
    file_name = give_a_name(url)
    text = get_text_resp(url)
    file_save(create_file_path(output, file_name), text)


def create_file_path(path, file_name):
    return os.path.join(path, file_name)


def get_text_resp(url):
    req = requests.get(url)
    return req.text


def file_save(file_path, data):
    with open(file_path, 'w') as output_file:
        output_file.write(data)


def give_a_name(url): # add orher urls cornet cases
    if 'http://' in url:
        url = url[7:]
    elif 'https://' in url:
        url = url[8:]
    return re.sub(r'[^a-zA-z0-9]', '-', url) + '.html'
