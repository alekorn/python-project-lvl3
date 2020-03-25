from page_loader.engine import normalize_url, arg_parse, page_load
import sys
import tempfile
import os


def test_normalize_url():
    assert normalize_url('https://hexlet.io/courses')  == 'hexlet-io-courses'
    assert normalize_url('http://hexlet.io/courses')  == 'hexlet-io-courses'
    assert normalize_url('hexlet.io/courses.html')  == 'hexlet-io-courses.html'
    assert normalize_url('https://hexlet.io/A1234567890.html')  == 'hexlet-io-A1234567890.html'


def test_arg_parse():
    args = arg_parse(['-o=/tmp/test/', 'https://hexlet.io/courses'])
    assert args.url == 'https://hexlet.io/courses'
    assert args.output == '/tmp/test/'


def test_page_load():
    with tempfile.TemporaryDirectory() as tmp_dir:
        page_load(tmp_dir, 'https://ru.hexlet.io/courses')
        assert os.path.exists(f'{tmp_dir}/ru-hexlet-io-courses.html')
        assert os.path.exists(f'{tmp_dir}/ru-hexlet-io-courses_files/')
        assert os.path.exists(f'{tmp_dir}/ru-hexlet-io-courses_files/ru-hexlet-io-lessons.rss')
