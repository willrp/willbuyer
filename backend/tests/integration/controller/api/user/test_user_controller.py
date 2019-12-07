from flask import json
from flask_login import current_user

from backend.util.response.user import UserSchema
from backend.util.response.error import ErrorSchema


def test_user_controller_current(flask_app, auth_user):
    with flask_app.test_client(user=auth_user) as client:
        response = client.get(
            "/api/user/current"
        )

        assert current_user.is_authenticated is True
        assert current_user == auth_user

    data = json.loads(response.data)
    UserSchema().load(data)

    assert response.status_code == 200


def test_user_controller_current_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.get(
            "/api/user/current"
        )

        assert current_user.is_authenticated is False

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
