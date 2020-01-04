from flask import json, session
from uuid import uuid4

from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema


def test_update_controller(flask_app, es_create):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id_2 = prod_list[1].meta["id"]

    with flask_app.test_client() as client:
        response = client.post(
            "api/cart/update/%s/1" % item_id
        )

        data = json.loads(response.data)
        CartSchema().load(data)
        assert response.status_code == 200
        assert session["cart"][item_id] == 1
        assert len(session["cart"]) == 1

        response = client.post(
            "api/cart/update/%s/5" % item_id_2
        )

        data = json.loads(response.data)
        CartSchema().load(data)
        assert response.status_code == 200
        assert session["cart"][item_id] == 1
        assert session["cart"][item_id_2] == 5
        assert len(session["cart"]) == 2

        response = client.post(
            "api/cart/update/%s/10" % item_id
        )

        data = json.loads(response.data)
        CartSchema().load(data)
        assert response.status_code == 200
        assert session["cart"][item_id] == 10
        assert session["cart"][item_id_2] == 5
        assert len(session["cart"]) == 2

        bad_item_id = str(uuid4())

        response = client.post(
            "api/cart/update/%s/1000" % bad_item_id
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400
        assert session["cart"][item_id] == 10
        assert session["cart"][item_id_2] == 5
        assert len(session["cart"]) == 2
