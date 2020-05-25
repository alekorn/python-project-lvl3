import os
from urllib.parse import urlparse

from progress.bar import IncrementalBar

from page_loader.document import get_name, download
from page_loader.logger import LOGGER, KnownError


def save_page(file_path, data):
    try:
        with open(file_path, 'w') as output_file:
            output_file.write(data)
    except OSError as error:
        LOGGER.error(error)
        raise KnownError(error)
    else:
        LOGGER.info(f"page saved {file_path}")


def save_file(file_path, data):
    try:
        with open(file_path, 'wb') as output_file:
            output_file.write(data)
    except OSError as error:
        LOGGER.error(error)
        raise KnownError(error)
    else:
        LOGGER.info(f"file saved {file_path}")


def save_content(content_list, dir_path, url):
    with IncrementalBar('Processing', max=len(content_list)) as bar:
        for attr_text in content_list:
            parse_attr = urlparse(attr_text)
            if parse_attr.scheme:
                data = download(attr_text)
            else:
                data = download(url + '/' + attr_text)
            file_path = os.path.join(dir_path, get_name(attr_text))
            save_file(file_path, data)
            bar.next()


def create_dir(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError as error:
        LOGGER.error(error)
        raise KnownError(error)
    else:
        LOGGER.warning(f"directory created {dir_path}")
