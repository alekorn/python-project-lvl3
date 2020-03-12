import argparse
import requests
import re


def arg_parse():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument(
        '-o',
        '--output',
        help='',
        type=str,
        default='default'
    )
    parser.add_argument('url', type=str, help='')
    args = parser.parse_args()
    return args.output, args.url


def run():
    return 'Hello world'


def get_text_resp(url):
    req = requests.get(url)
    return req.text


def file_save(file_path, data):
    with open(file_path, 'w') as output_file:
        output_file.write(data)


def give_a_name(url):
    if 'http://' in url:
        url = url[7:]
    elif 'https://' in url:
        url = url[8:]
    return re.sub(r'[^a-zA-z0-9]', '-', url) + '.html'
