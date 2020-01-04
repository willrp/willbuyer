import pytest
import requests
from json.decoder import JSONDecodeError

from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema


def test_remove(domain_url, es_create):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id_2 = prod_list[1].meta["id"]

    with requests.Session() as sess:
        sess.verify = False

        response = sess.get(
            domain_url
        )

        cookie = response.cookies.get("session")

        response = sess.post(
            domain_url + "/api/cart/update/%s/15" % item_id
        )

        data = response.json()
        CartSchema().load(data)
        assert response.status_code == 200
        assert cookie != response.cookies.get("session")

        cookie = response.cookies.get("session")

        response = sess.post(
            domain_url + "/api/cart/update/%s/3" % item_id_2
        )

        data = response.json()
        CartSchema().load(data)
        assert response.status_code == 200
        assert cookie != response.cookies.get("session")

        cookie = response.cookies.get("session")

        response = sess.post(
            domain_url + "/api/cart/remove/%s" % item_id
        )

        data = response.json()
        CartSchema().load(data)
        assert response.status_code == 200
        assert cookie != response.cookies.get("session")

        cookie = response.cookies.get("session")

        response = sess.post(
            domain_url + "/api/cart/remove/invalid"
        )

        data = response.json()
        ErrorSchema().load(data)
        assert response.status_code == 400
        assert cookie != response.cookies.get("session")

        response = sess.post(
            domain_url + "/api/cart/remove/%s" % item_id_2
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204
        assert cookie != response.cookies.get("session")
