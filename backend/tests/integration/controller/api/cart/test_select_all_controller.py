import pytest
from flask import json
from json.decoder import JSONDecodeError

from backend.util.response.cart import CartSchema


def test_select_all_controller(flask_app, es_create):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id_2 = prod_list[1].meta["id"]

    with flask_app.test_client() as client:
        response = client.get(
            "api/cart"
        )

        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        assert response.status_code == 204

        with client.session_transaction() as sess:
            assert "cart" not in sess
            sess["cart"] = {item_id: 1, item_id_2: 2}
            assert sess["cart"][item_id] == 1
            assert sess["cart"][item_id_2] == 2

        response = client.get(
            "api/cart"
        )

        data = json.loads(response.data)
        CartSchema().load(data)
        assert response.status_code == 200

        for item in data["products"]:
            assert item["id"] in [item_id, item_id_2]
            assert item["amount"] in [1, 2]
