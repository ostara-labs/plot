from plot_backend import greet


def test_greet():
    assert greet("template") == "Hello, template!"
