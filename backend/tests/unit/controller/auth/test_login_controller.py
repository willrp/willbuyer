import pytest
import re
import responses
import json
from unittest.mock import MagicMock
from flask_dance.consumer.storage import MemoryStorage
from flask_login import current_user
from oauthlib.oauth2 import InvalidGrantError, MissingCodeError, MismatchingStateError
from sqlalchemy.exc import DatabaseError

from backend.service import UserService
from backend.controller.auth import login_manager, refresh_user_logged_in
from backend.controller.auth.login import bplogin, user_logged_in
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="function", autouse=True)
def controller_mocker(mocker):
    mocker.patch.object(UserService, "__init__", return_value=None)


@pytest.fixture(scope="function")
def memory_blueprint(monkeypatch):
    storage = MemoryStorage({"access_token": "fake-token"})
    monkeypatch.setattr(bplogin, "storage", storage)
    return bplogin


def test_login_controller_authorized(mocker, flask_app, memory_blueprint):
    mocker.patch.object(UserService, "get_create_oauth", return_value=MagicMock(autospec=True))
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(".+google.+"),
            status=200,
            json={
                "id": "fake-id"
            }
        )

        with flask_app.test_request_context("/auth/google/authorized"):
            returned = user_logged_in(memory_blueprint, {"access_token": "fake-token"})

    assert returned is False


def test_login_controller_authorized_no_token(flask_app):
    with flask_app.test_request_context("/auth/google/authorized"):
        assert current_user.is_authenticated is False
        returned = user_logged_in(bplogin, None)
        assert current_user.is_authenticated is False

    assert returned is not False
    assert re.search(r"error=token$", returned.headers["Location"]) is not None
    assert returned.status_code == 302


def test_login_controller_authorized_not_ok(flask_app, memory_blueprint):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(".+google.+"),
            status=400
        )

        with flask_app.test_request_context("/auth/google/authorized"):
            assert current_user.is_authenticated is False
            returned = user_logged_in(memory_blueprint, {"access_token": "fake-token"})
            assert current_user.is_authenticated is False

    assert returned is not False
    assert re.search(r"error=error$", returned.headers["Location"]) is not None
    assert returned.status_code == 302


def test_login_controller_authorized_error(mocker, flask_app, memory_blueprint):
    mocker.patch.object(UserService, "get_create_oauth", side_effect=DatabaseError("statement", "params", "orig"))
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(".+google.+"),
            status=200
        )

        with flask_app.test_request_context("/auth/google/authorized"):
            assert current_user.is_authenticated is False
            returned = user_logged_in(memory_blueprint, {"access_token": "fake-token"})
            assert current_user.is_authenticated is False

    assert returned is not False
    assert re.search(r"error=error$", returned.headers["Location"]) is not None
    assert returned.status_code == 302


def test_login_controller_login(flask_app):
    with flask_app.test_client() as client:
        with client.session_transaction() as sess:
            assert sess.get("next_url") is None

        response = client.get(
            "auth/login"
        )

        with client.session_transaction() as sess:
            assert sess.get("next_url") is None

    assert re.search(r"google_login", response.headers["Location"]) is not None
    assert response.status_code == 302


def test_login_controller_login_next(flask_app):
    with flask_app.test_client() as client:
        with client.session_transaction() as sess:
            assert sess.get("next_url") is None

        response = client.get(
            "auth/login?next=willroger"
        )

        with client.session_transaction() as sess:
            assert sess.get("next_url") == "willroger"

    assert re.search(r"google_login", response.headers["Location"]) is not None
    assert response.status_code == 302


def test_login_controller_login_logged_in(flask_app, auth_user):
    with flask_app.test_client(user=auth_user) as client:
        response = client.get(
            "auth/login"
        )

    assert re.search(r"google_login", response.headers["Location"]) is None
    assert response.status_code == 302


def test_login_controller_user_logged_in(flask_app):
    with flask_app.test_request_context("/auth/login"):
        assert login_manager.refresh_view is None
        refresh_user_logged_in()
        assert login_manager.refresh_view == "google.login"
        login_manager.refresh_view = None


@pytest.mark.parametrize(
    "error",
    [
        (MissingCodeError()),
        (MismatchingStateError())
    ]
)
def test_login_controller_missing_mismatching(mocker, flask_app, error):
    with mocker.patch("flask_dance.consumer.oauth2.redirect", side_effect=error):
        with flask_app.test_client() as client:
            response = client.get(
                "auth/google/authorized"
            )

        assert re.search(r"google_login", response.headers["Location"]) is not None
        assert response.status_code == 302


def test_login_controller_invalid_grant(monkeypatch, mocker, flask_app, test_vcr):
    storage = MemoryStorage({"access_token": "fake-token"})
    monkeypatch.setattr(bplogin, "storage", storage)

    with test_vcr.use_cassette("auth_google_token_revoke_fake.yml"):
        with mocker.patch("flask_dance.consumer.oauth2.redirect", side_effect=InvalidGrantError()):
            with flask_app.test_client() as client:
                response = client.get(
                    "auth/google/authorized"
                )

        assert re.search(r"google_login", response.headers["Location"]) is not None
        assert response.status_code == 302


@pytest.mark.parametrize(
    "test_url, error, status_code",
    [
        ("/auth/login", Exception(), 500)
    ]
)
def test_login_controller_error(mocker, flask_app, test_url, error, status_code):
    with mocker.patch("flask_login.utils._get_user", side_effect=error):
        with flask_app.test_client() as client:
            response = client.get(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)

        assert response.status_code == status_code
