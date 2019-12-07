import requests
from uuid import uuid4

from backend.util.response.error import ErrorSchema


def test_update(domain_url, auth_session, es_create):
    prod_list = es_create("products", 1)
    item_id = prod_list[0].meta["id"]

    response = auth_session.get(
        domain_url
    )

    cookie = response.cookies.get("session")

    response = auth_session.post(
        domain_url + "/api/cart/update/%s/1" % item_id
    )

    assert response.status_code == 200
    assert cookie != response.cookies.get("session")

    cookie = response.cookies.get("session")

    response = auth_session.post(
        domain_url + "/api/cart/update/%s/10" % item_id
    )

    assert response.status_code == 200
    assert cookie != response.cookies.get("session")

    cookie = response.cookies.get("session")

    bad_item_id = str(uuid4())

    response = auth_session.post(
        domain_url + "/api/cart/update/%s/1" % bad_item_id
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 400
    assert cookie == response.cookies.get("session")


def test_update_unauthorized(domain_url):
    response = requests.post(
        domain_url + "/api/cart/update/test/1",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
