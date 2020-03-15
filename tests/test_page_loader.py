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


# def test_text_resp():
#     pass
#
#
# def test_file_save():
#     pass
