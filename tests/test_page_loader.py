from page_loader.engine import run, give_a_name


def test_page_loader():
    assert run()  == 'Hello world'


def test_give_a_name():
    assert give_a_name('https://hexlet.io/courses')  == 'hexlet-io-courses.html'
    assert give_a_name('http://hexlet.io/courses')  == 'hexlet-io-courses.html'
    assert give_a_name('hexlet.io/courses')  == 'hexlet-io-courses.html'
    assert give_a_name('https://hexlet.io/A1234567890')  == 'hexlet-io-A1234567890.html'



# def test_page_loader():
#     assert run()  == 'Hello world'
# def test_page_loader():
#     assert run()  == 'Hello world'
# def test_page_loader():
#     assert run()  == 'Hello world'
# def test_page_loader():
#     assert run()  == 'Hello world'
# def test_page_loader():
#     assert run()  == 'Hello world'
# def test_page_loader():
#     assert run()  == 'Hello world'
