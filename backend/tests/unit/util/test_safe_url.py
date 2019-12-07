import pytest

from backend.util.safe_url import is_safe_url


@pytest.mark.parametrize(
    "safe_url",
    [
        ("http://localhost"),
        ("http://localhost/will"),
        ("/will"),
        ("will"),
        (None)
    ]
)
def test_safe_url(flask_app, safe_url):
    with flask_app.test_request_context():
        assert is_safe_url(safe_url) is True


@pytest.mark.parametrize(
    "safe_url",
    [
        ("http://localhost"),
        ("http://localhost/will"),
        ("/will"),
        ("will"),
        (None)
    ]
)
def test_safe_url_no_context(safe_url):
    assert is_safe_url(safe_url) is False


def test_unsafe_url(flask_app):
    with flask_app.test_request_context():
        assert is_safe_url("http://willbuyer.herokuapp.com") is False
