from page_loader.engine import normalize_url, arg_parse, page_load, get_data, TAGS_ATTRS
import sys
import tempfile
import os
from bs4 import BeautifulSoup

URL1 = 'alekorn.github.io/alekorn-tests-page1.html'
URL2 = 'alekorn.github.io/alekorn-tests-page1'
NORM_FILES = 'alekorn-github-io-alekorn-tests-page1_files'
NORM_URL1 = 'alekorn-github-io-alekorn-tests-page1.html'
NORM_URL2 = 'alekorn-github-io-alekorn-tests-page1'
NORM_FILE1 = 'css-main.css'
NORM_FILE2 = 's3-us-west-2-amazonaws-com-s-cdpn-io-1425525-789p0uP.png'
NORM_FILE3 = 'i-imgur-com-789p0uP.png'


def txt_load(file):
    with open(file, "r") as read_file:
        data = read_file.read().rstrip()
    return data


def test_normalize_url():
    assert normalize_url(f'http://{URL1}')  == NORM_URL1
    assert normalize_url(URL2)  == NORM_URL2
    assert normalize_url(f'https://{URL2}')  == NORM_URL2
    assert normalize_url(f'http://{URL2}')  == NORM_URL2


def test_arg_parse():
    args = arg_parse(['-o=/tmp/test/', f'https://{URL2}'])
    assert args.url == f'https://{URL2}'
    assert args.output == '/tmp/test/'
    assert args.log == 'warning'
    args = arg_parse(['-o=/tmp/test/', f'https://{URL2}', '-l=error'])
    assert args.log == 'error'


def test_page_load():
    with tempfile.TemporaryDirectory() as tmp_dir:
        page_load(tmp_dir, f'https://{URL2}')
        assert os.path.exists(f'{tmp_dir}/{NORM_URL1}')
        assert os.path.exists(f'{tmp_dir}/{NORM_FILES}/')
        assert os.path.exists(f'{tmp_dir}/{NORM_FILES}/{NORM_FILE1}')
        assert os.path.exists(f'{tmp_dir}/{NORM_FILES}/{NORM_FILE2}')
        assert os.path.exists(f'{tmp_dir}/{NORM_FILES}/{NORM_FILE3}')
        text = txt_load(f'{tmp_dir}/{NORM_URL1}')
        attr_list, _ = get_data(text, TAGS_ATTRS, '_')
        assert attr_list == [
                f'{NORM_FILES}/{NORM_FILE1}',
                f'{NORM_FILES}/{NORM_FILE2}',
                f'{NORM_FILES}/{NORM_FILE3}'
                ]
