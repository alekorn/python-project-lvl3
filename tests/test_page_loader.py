from page_loader.engine import give_a_name, arg_parse, page_loader
import sys
import tempfile
import os


def test_give_a_name():
    assert give_a_name('https://hexlet.io/courses')  == 'hexlet-io-courses.html'
    assert give_a_name('http://hexlet.io/courses')  == 'hexlet-io-courses.html'
    assert give_a_name('hexlet.io/courses')  == 'hexlet-io-courses.html'
    assert give_a_name('https://hexlet.io/A1234567890')  == 'hexlet-io-A1234567890.html'


def test_arg_parse():
    args = arg_parse(['-o=/tmp/test/', 'https://hexlet.io/courses'])
    assert args.url == 'https://hexlet.io/courses'
    assert args.output == '/tmp/test/'


def test_page_loader():
    with tempfile.TemporaryDirectory() as tmp_dir:
        page_loader(tmp_dir, 'https://hexlet.io/courses')
        assert os.path.exists(f'{tmp_dir}/hexlet-io-courses.html')


def test_page_loader2():
    with tempfile.TemporaryDirectory() as tmp_dir:
        page_loader(tmp_dir, 'https://hexlet.io/courses')
        assert os.path.exists(f'{tmp_dir}/hexlet-io-courses-files/')
        assert os.path.exists(f'{tmp_dir}/hexlet-io-courses-files/cdn2-hexlet-io-assets-favicon-8fa102c058afb01de5016a155d7db433283dc7e08ddc3c4d1aef527c1b8502b6.ico"')
