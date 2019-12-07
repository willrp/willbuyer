import requests

from backend.util.response.error import ErrorSchema


def test_order(domain_url, auth_session, es_create, willorders_ws_db_session):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id2 = prod_list[1].meta["id"]

    auth_session.post(
        domain_url + "/api/cart/update/%s/1" % item_id
    )

    response = auth_session.post(
        domain_url + "/api/cart/update/%s/2" % item_id2
    )

    cookie = response.cookies.get("session")

    response = auth_session.put(
        domain_url + "/api/cart/order"
    )

    data = response.json()
    assert data == {}
    assert response.status_code == 201
    assert cookie != response.cookies.get("session")

    cookie = response.cookies.get("session")

    response = auth_session.put(
        domain_url + "/api/cart/order"
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 400
    assert cookie == response.cookies.get("session")


def test_order_unauthorized(domain_url):
    response = requests.put(
        domain_url + "/api/cart/order",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
