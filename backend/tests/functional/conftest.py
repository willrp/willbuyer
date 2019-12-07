import pytest
import requests


@pytest.fixture(scope="session")
def domain_url(flask_app, domain_ip):
    return "https://" + domain_ip + ":8000"


@pytest.fixture(scope="function")
def auth_session(flask_app, auth_user):
    with flask_app.test_client(user=auth_user) as client:
        response = client.get(
            "/"
        )

    cookie = response.headers["Set-Cookie"].split("=")

    sess = requests.Session()
    sess.cookies.set(cookie[0], cookie[1])
    sess.verify = False
    return sess
