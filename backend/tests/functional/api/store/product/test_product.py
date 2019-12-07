import requests
from uuid import uuid4

from backend.util.response.store.product_results import ProductResultsSchema
from backend.util.response.error import ErrorSchema


def test_product_controller(domain_url, es_create, auth_session):
    prod_list = es_create("products", 3)
    prod_id = prod_list[0].meta["id"]

    response = auth_session.get(
        domain_url + "/api/store/product/%s" % prod_id
    )

    data = response.json()
    ProductResultsSchema().load(data)
    assert response.status_code == 200

    response = auth_session.get(
        domain_url + "/api/store/product/%s" % str(uuid4())
    )

    data = response.json()
    assert data["error"] == {}
    assert response.status_code == 404


def test_product_controller_unauthorized(domain_url):
    response = requests.get(
        domain_url + "/api/store/product/test",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
