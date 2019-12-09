import pytest
from flask import json
from unittest.mock import MagicMock

from backend.util.response.user import UserSchema
from backend.util.response.error import ErrorSchema


def mock_to_dict():
    return {
        "email": "will@willbuyer.com",
        "name": "Test User",
        "picture": "https://lh5.googleusercontent.com/-y3L400P9hhs/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rd6hI7NP9rpbi3VsSDkUVx18WLjgw/s96-cc-rg/photo.jpg"
    }


def test_user_controller_current(mocker, login_disabled_app):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(to_dict=mock_to_dict))
    with login_disabled_app.test_client() as client:
        response = client.get(
            "/api/user/current"
        )

    data = json.loads(response.data)
    UserSchema().load(data)

    assert response.status_code == 200


@pytest.mark.parametrize(
    "test_url, error, status_code",
    [
        ("/api/user/current", Exception(), 500)
    ]
)
def test_users_controller_current_error(mocker, login_disabled_app, test_url, error, status_code):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(to_dict=MagicMock(side_effect=error)))
    with login_disabled_app.test_client() as client:
        response = client.get(
            test_url
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == status_code
