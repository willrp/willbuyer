import pytest
import requests
from json.decoder import JSONDecodeError

from backend.util.response.cart import CartSchema


def test_select_all(domain_url, es_create):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id2 = prod_list[1].meta["id"]

    with requests.Session() as sess:
        sess.verify = False

        response = sess.get(
            domain_url + "/api/cart",
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

        response = sess.post(
            domain_url + "/api/cart/update/%s/1" % item_id
        )

        assert response.status_code == 200

        response = sess.post(
            domain_url + "/api/cart/update/%s/2" % item_id2
        )

        assert response.status_code == 200

        response = sess.get(
            domain_url + "/api/cart",
        )

        data = response.json()
        CartSchema().load(data)
        assert response.status_code == 200

        for item in data["products"]:
            assert item["id"] in [item_id, item_id2]
            assert item["amount"] in [1, 2]
