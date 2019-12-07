from flask import json, session

from backend.util.response.error import ErrorSchema


def test_order_controller(flask_app, auth_user, es_create, willorders_ws_db_session):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id2 = prod_list[1].meta["id"]

    with flask_app.test_client(user=auth_user) as client:
        with client.session_transaction() as sess:
            sess["cart"] = {item_id: 1, item_id2: 2}
            assert sess["cart"][item_id] == 1
            assert sess["cart"][item_id2] == 2

        response = client.put(
            "api/cart/order"
        )

        data = json.loads(response.data)
        assert data == {}
        assert response.status_code == 201
        assert session["cart"] == {}

        response = client.put(
            "api/cart/order"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400

        with client.session_transaction() as sess:
            sess["cart"] = {"notregistered": 1}
            assert sess["cart"]["notregistered"] == 1

        response = client.put(
            "api/cart/order"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400
        assert session["cart"]["notregistered"] == 1


def test_order_controller_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.put(
            "api/cart/order"
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
