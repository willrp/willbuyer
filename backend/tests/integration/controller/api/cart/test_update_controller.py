from flask import json, session
from uuid import uuid4

from backend.util.response.error import ErrorSchema


def test_update_controller(flask_app, auth_user, es_create):
    prod_list = es_create("products", 1)
    item_id = prod_list[0].meta["id"]

    with flask_app.test_client(user=auth_user) as client:
        with client.session_transaction() as sess:
            assert "cart" not in sess

        response = client.post(
            "api/cart/update/%s/1" % item_id
        )

        assert response.status_code == 200
        assert session["cart"][item_id] == 1

        response = client.post(
            "api/cart/update/%s/10" % item_id
        )

        assert response.status_code == 200
        assert session["cart"][item_id] == 10

    bad_item_id = str(uuid4())

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/cart/update/%s/1" % bad_item_id
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400

        assert "cart" not in sess


def test_update_controller_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.post(
            "api/cart/update/test/1",
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
