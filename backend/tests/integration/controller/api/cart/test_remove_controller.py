import pytest
from flask import json, session
from json.decoder import JSONDecodeError

from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema


def test_remove_controller(flask_app, es_create):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id_2 = prod_list[1].meta["id"]

    with flask_app.test_client() as client:
        with client.session_transaction() as sess:
            assert "cart" not in sess
            sess["cart"] = {item_id: 1, item_id_2: 2}
            assert sess["cart"][item_id] == 1
            assert sess["cart"][item_id_2] == 2
            assert len(sess["cart"]) == 2

        response = client.post(
            "api/cart/remove/%s" % item_id
        )

        data = json.loads(response.data)
        CartSchema().load(data)
        assert response.status_code == 200
        assert item_id not in session["cart"]
        assert session["cart"][item_id_2] == 2
        assert len(session["cart"]) == 1

        response = client.post(
            "api/cart/remove/%s" + item_id
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400
        assert item_id not in session["cart"]
        assert session["cart"][item_id_2] == 2
        assert len(session["cart"]) == 1

        response = client.post(
            "api/cart/remove/%s" % item_id_2
        )

        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        assert response.status_code == 204
        assert item_id not in session["cart"]
        assert item_id_2 not in session["cart"]
        assert len(session["cart"]) == 0
