import pytest
import re
import responses
from flask import json
from unittest.mock import MagicMock
from flask_dance.consumer.storage import MemoryStorage
from oauthlib.oauth2 import TokenExpiredError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from backend.controller.auth import bplogin
from backend.util.response.error import ErrorSchema


def test_logout_controller(monkeypatch, mocker, login_disabled_app):
    storage = MemoryStorage({"access_token": "fake-token"})
    monkeypatch.setattr(bplogin, "storage", storage)
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(provider="google", autospec=True))
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(".+google.+"),
            status=200
        )

        with login_disabled_app.test_client() as client:
            response = client.get(
                "/auth/logout"
            )

    assert response.status_code == 302


@pytest.mark.parametrize(
    "error",
    [
        (TokenExpiredError()),
        (HTTPException()),
        (Exception())
    ]
)
def test_logout_controller_token_exception(monkeypatch, mocker, login_disabled_app, error):
    storage = MemoryStorage({"access_token": "fake-token"})
    monkeypatch.setattr(bplogin, "storage", storage)

    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(provider="google", autospec=True))
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(".+google.+"),
            body=error
        )

        with login_disabled_app.test_client() as client:
            response = client.get(
                "/auth/logout"
            )

    assert response.status_code == 302


@pytest.mark.parametrize(
    "test_url, error, status_code",
    [
        ("/auth/logout", SQLAlchemyError(), 504),
        ("/auth/logout", Exception(), 500)
    ]
)
def test_logout_controller_error(monkeypatch, mocker, login_disabled_app, test_url, error, status_code):
    storage = MemoryStorage({"access_token": "fake-token"})
    monkeypatch.setattr(bplogin, "storage", storage)

    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(provider="google", autospec=True))
    mocker.patch("backend.controller.auth.logout.logout_user", new=MagicMock(side_effect=error))
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(".+google.+"),
            status=200
        )

        with login_disabled_app.test_client() as client:
            response = client.get(
                "/auth/logout"
            )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == status_code


def test_logout_controller_unauthenticated(flask_app):
    with flask_app.test_client() as client:
        response = client.get(
            "/auth/logout"
        )

        assert re.search(r"cognito_login", response.headers.get("Location")) is None
        assert re.search(r"google_login", response.headers.get("Location")) is None
        assert response.status_code == 302
