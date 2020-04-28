from page_loader.getters import get_name, get_data
from page_loader.engine import page_load, arg_parse, TAGS_ATTRS, normalize_url
from page_loader.logger import KnownError
from page_loader.savers import save_page, save_file, create_dir
import sys
import tempfile
import os
from bs4 import BeautifulSoup
import pytest

URL1 = 'alekorn.github.io/alekorn-tests-page1.html'
URL2 = 'alekorn.github.io/alekorn-tests-page1'
PATH_FILES = 'alekorn-github-io-alekorn-tests-page1_files'
PATH_URL1 = 'alekorn-github-io-alekorn-tests-page1.html'
PATH_URL2 = 'alekorn-github-io-alekorn-tests-page1'
PATH_FILE1 = 'css-main.css'
PATH_FILE2 = 's3-us-west-2-amazonaws-com-s-cdpn-io-1425525-789p0uP.png'
PATH_FILE3 = 'i-imgur-com-789p0uP.png'


def txt_load(file):
    with open(file, "r") as read_file:
        data = read_file.read().rstrip()
    return data


def test_normalize_url():
    assert normalize_url('google.com')  == 'http://google.com'
    assert normalize_url('http://google.com')  == 'http://google.com'
    assert normalize_url('https://google.com')  == 'https://google.com'


def test_get_name():
    assert get_name(f'http://{URL1}')  == PATH_URL1
    assert get_name(URL2)  == PATH_URL2
    assert get_name(f'https://{URL2}')  == PATH_URL2
    assert get_name(f'http://{URL2}')  == PATH_URL2


def test_arg_parse():
    args = arg_parse(['-o=/tmp/test/', f'https://{URL2}'])
    assert args.url == f'https://{URL2}'
    assert args.output == '/tmp/test/'
    assert args.log == 'info'
    args = arg_parse(['-o=/tmp/test/', f'https://{URL2}', '-l=error'])
    assert args.log == 'error'


def test_page_load():
    with tempfile.TemporaryDirectory() as tmp_dir:
        page_load(tmp_dir, URL2)
        assert os.path.exists(os.path.join(tmp_dir, PATH_URL1))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES, PATH_FILE1))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES, PATH_FILE2))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES, PATH_FILE3))
        text = txt_load(os.path.join(tmp_dir, PATH_URL1))
        attr_list, _ = get_data(text, TAGS_ATTRS, '_')
        assert attr_list == [
                os.path.join(PATH_FILES, PATH_FILE1),
                os.path.join(PATH_FILES, PATH_FILE2),
                os.path.join(PATH_FILES, PATH_FILE3)
                ]


def test_exceptions1():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno -2'):
            page_load(tmp_dir, 'https://nonexistent-page.bla')


def test_exceptions2():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='401'):
            page_load(tmp_dir, 'https://httpstat.us/401')
        with pytest.raises(KnownError, match='404'):
            page_load(tmp_dir, 'https://httpstat.us/404')
        with pytest.raises(KnownError, match='403'):
            page_load(tmp_dir, 'https://httpstat.us/403')
        with pytest.raises(KnownError, match='405'):
            page_load(tmp_dir, 'https://httpstat.us/405')
        with pytest.raises(KnownError, match='406'):
            page_load(tmp_dir, 'https://httpstat.us/406')
        with pytest.raises(KnownError, match='408'):
            page_load(tmp_dir, 'https://httpstat.us/408')
        with pytest.raises(KnownError, match='500'):
            page_load(tmp_dir, 'https://httpstat.us/500')
        with pytest.raises(KnownError, match='507'):
            page_load(tmp_dir, 'https://httpstat.us/507')


def test_exceptions3():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno 13'):
            page_load('/', 'http://google.com')
        with pytest.raises(KnownError, match='Errno 17'):
            os.mkdir(f'{tmp_dir}/google-com_files')
            page_load(tmp_dir, 'http://google.com/')


def test_exceptions4():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno 21'):
            save_page('/', '')


def test_exceptions5():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno 21'):
            save_file('/', '')
