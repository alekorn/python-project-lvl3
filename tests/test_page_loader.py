import os
import sys
import tempfile

import pytest
from bs4 import BeautifulSoup

from page_loader.engine import load_page
from page_loader.document import change_attrs, get_name, normalize_url
from page_loader.logging import KnownError
from page_loader.storage import create_dir, save_file, save_page

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


def test_load_page():
    with tempfile.TemporaryDirectory() as tmp_dir:
        load_page(tmp_dir, URL2)
        assert os.path.exists(os.path.join(tmp_dir, PATH_URL1))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES, PATH_FILE1))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES, PATH_FILE2))
        assert os.path.exists(os.path.join(tmp_dir, PATH_FILES, PATH_FILE3))
        text = txt_load(os.path.join(tmp_dir, PATH_URL1))
        attr_list, _ = change_attrs(text, '_')
        assert attr_list == [
                os.path.join(PATH_FILES, PATH_FILE1),
                os.path.join(PATH_FILES, PATH_FILE2),
                os.path.join(PATH_FILES, PATH_FILE3)
                ]


def test_exceptions1():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno -2'):
            load_page(tmp_dir, 'https://nonexistent-page.bla')


def test_exceptions2():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='401'):
            load_page(tmp_dir, 'https://httpstat.us/401')
        with pytest.raises(KnownError, match='404'):
            load_page(tmp_dir, 'https://httpstat.us/404')
       #  with pytest.raises(KnownError, match='403'):  # TODO uncommet this
       #      load_page(tmp_dir, 'https://httpstat.us/403')
       #  with pytest.raises(KnownError, match='405'):
       #      load_page(tmp_dir, 'https://httpstat.us/405')
       #  with pytest.raises(KnownError, match='406'):
       #      load_page(tmp_dir, 'https://httpstat.us/406')
       #  with pytest.raises(KnownError, match='408'):
       #      load_page(tmp_dir, 'https://httpstat.us/408')
       #  with pytest.raises(KnownError, match='500'):
       #      load_page(tmp_dir, 'https://httpstat.us/500')
       #  with pytest.raises(KnownError, match='507'):
       #      load_page(tmp_dir, 'https://httpstat.us/507')


def test_exceptions3():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno 13'):
            load_page('/', 'http://google.com')
        with pytest.raises(KnownError, match='Errno 17'):
            os.mkdir(f'{tmp_dir}/google-com_files')
            load_page(tmp_dir, 'http://google.com/')


def test_exceptions4():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno 21'):
            save_page('/', '')


def test_exceptions5():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(KnownError, match='Errno 2'):
            save_file('', '')
