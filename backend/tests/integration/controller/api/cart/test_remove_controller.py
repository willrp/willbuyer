from flask import json, session

from backend.util.response.error import ErrorSchema


def test_remove_controller(flask_app, auth_user):
    with flask_app.test_client(user=auth_user) as client:
        with client.session_transaction() as sess:
            assert "cart" not in sess
            sess["cart"] = {"test": 1}
            assert sess["cart"]["test"] == 1

        response = client.post(
            "api/cart/remove/test"
        )

        assert response.status_code == 200
        assert "test" not in session["cart"]

        response = client.post(
            "api/cart/remove/test"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400


def test_remove_controller_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.post(
            "api/cart/remove/test",
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
