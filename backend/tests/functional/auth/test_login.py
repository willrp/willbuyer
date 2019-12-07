import re
import requests


def test_login(domain_url):
    response = requests.get(
        domain_url + "/auth/login",
        allow_redirects=False,
        verify=False
    )

    location = response.headers.get("Location")
    assert re.search(r"google_login", location) is not None
    assert response.status_code == 302
    assert response.cookies.get("session") is None

    response = requests.get(
        domain_url + "/auth/login?next=willroger",
        allow_redirects=False,
        verify=False
    )

    assert re.search(r"google_login", response.headers.get("Location")) is not None
    assert response.status_code == 302
    assert response.cookies.get("session") is not None

    response = requests.get(
        location,
        allow_redirects=False,
        verify=False
    )

    assert re.search(r"accounts\.google", response.headers.get("Location")) is not None
    assert response.status_code == 302
