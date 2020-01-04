import requests
from uuid import uuid4

from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema


def test_update(domain_url, es_create):
    prod_list = es_create("products", 1)
    item_id = prod_list[0].meta["id"]

    with requests.Session() as sess:
        sess.verify = False

        response = sess.get(
            domain_url
        )

        cookie = response.cookies.get("session")

        response = sess.post(
            domain_url + "/api/cart/update/%s/1" % item_id
        )

        data = response.json()
        CartSchema().load(data)
        assert response.status_code == 200
        assert cookie != response.cookies.get("session")

        cookie = response.cookies.get("session")

        response = sess.post(
            domain_url + "/api/cart/update/%s/10" % item_id
        )

        data = response.json()
        CartSchema().load(data)
        assert response.status_code == 200
        assert cookie != response.cookies.get("session")

        cookie = response.cookies.get("session")

        bad_item_id = str(uuid4())

        response = sess.post(
            domain_url + "/api/cart/update/%s/1" % bad_item_id
        )

        data = response.json()
        ErrorSchema().load(data)
        assert response.status_code == 400
        assert response.cookies.get("session") is None
