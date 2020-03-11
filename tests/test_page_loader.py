from page_loader.engine import run


def test_page_loader():
    assert run()  == 'Hello world'
