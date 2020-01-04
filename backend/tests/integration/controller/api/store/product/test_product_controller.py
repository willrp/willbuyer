from flask import json
from uuid import uuid4

from backend.util.response.store.product_results import ProductResultsSchema


def test_product_controller(flask_app, es_create):
    prod_list = es_create("products", 3)
    prod_id = prod_list[0].meta["id"]

    with flask_app.test_client() as client:
        response = client.get(
            "api/store/product/%s" % prod_id
        )

    data = json.loads(response.data)
    ProductResultsSchema().load(data)
    assert response.status_code == 200

    with flask_app.test_client() as client:
        response = client.get(
            "api/store/product/%s" % str(uuid4())
        )

    data = json.loads(response.data)
    assert data["error"] == {}
    assert response.status_code == 404
