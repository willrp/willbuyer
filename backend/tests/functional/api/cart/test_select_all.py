import pytest
import requests
from json.decoder import JSONDecodeError

from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema


def test_select_all(domain_url, auth_session, es_create):
    prod_list = es_create("products", 2)
    item_id = prod_list[0].meta["id"]
    item_id2 = prod_list[1].meta["id"]

    response = auth_session.get(
        domain_url + "/api/cart"
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    response = auth_session.post(
        domain_url + "/api/cart/update/%s/1" % item_id
    )

    assert response.status_code == 200

    response = auth_session.post(
        domain_url + "/api/cart/update/%s/2" % item_id2
    )

    assert response.status_code == 200

    response = auth_session.get(
        domain_url + "/api/cart"
    )

    data = response.json()
    CartSchema().load(data)
    assert response.status_code == 200

    for item in data["item_list"]:
        assert item["item_id"] in [item_id, item_id2]
        assert item["amount"] in [1, 2]


def test_select_all_unauthorized(domain_url):
    response = requests.get(
        domain_url + "/api/cart",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
