import requests
from uuid import uuid4

from backend.util.response.store.product_results import ProductResultsSchema


def test_product_controller(domain_url, es_create):
    prod_list = es_create("products", 3)
    prod_id = prod_list[0].meta["id"]

    response = requests.get(
        domain_url + "/api/store/product/%s" % prod_id,
        verify=False
    )

    data = response.json()
    ProductResultsSchema().load(data)
    assert response.status_code == 200

    response = requests.get(
        domain_url + "/api/store/product/%s" % str(uuid4()),
        verify=False
    )

    data = response.json()
    assert data["error"] == {}
    assert response.status_code == 404
