import os

from page_loader.document import (
        change_attrs,
        download,
        get_name,
        normalize_url
        )
from page_loader.storage import create_dir, save_content, save_page


def load_page(output, url):
    url = normalize_url(url)
    name = get_name(url)
    file_name = f'{name}.html'
    dir_name = f'{name}_files'
    file_path = os.path.join(output, file_name)
    dir_path = os.path.join(output, dir_name)
    page_text = download(url)
    create_dir(dir_path)
    content_list, data = change_attrs(page_text, dir_name)
    save_page(file_path, data)
    save_content(content_list, dir_path, url)
