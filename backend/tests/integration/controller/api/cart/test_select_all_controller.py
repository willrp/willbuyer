import pytest
from flask import json
from json.decoder import JSONDecodeError

from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema


def test_select_all_controller(flask_app, auth_user):
    with flask_app.test_client(user=auth_user) as client:
        response = client.get(
            "api/cart"
        )

        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        assert response.status_code == 204

        with client.session_transaction() as sess:
            assert "cart" not in sess
            sess["cart"] = {"test": 1, "test2": 2}
            assert sess["cart"]["test"] == 1
            assert sess["cart"]["test2"] == 2

        response = client.get(
            "api/cart"
        )

        data = json.loads(response.data)
        CartSchema().load(data)
        assert response.status_code == 200

        for item in data["item_list"]:
            assert item["item_id"] in ["test", "test2"]
            assert item["amount"] in [1, 2]


def test_select_all_controller_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.get(
            "api/cart",
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
