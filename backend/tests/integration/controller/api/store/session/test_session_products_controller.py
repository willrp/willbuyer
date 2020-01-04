import pytest
from flask import json
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.search_products_results import SearchProductsResultsSchema


def test_session_products_controller(flask_app, es_create):
    session_list = es_create("sessions", 3, gender="Women")
    session_id = session_list[0].meta["id"]
    es_create("products", 5, gender="Women", sessionid=session_id)

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s/1" % (session_id)
        )

    data = json.loads(response.data)
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 5

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s/1" % (session_id),
            json={
                "pricerange": {
                    "min": 1,
                    "max": 500
                },
                "pagesize": 1
            }
        )

    data = json.loads(response.data)
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 1

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s/10" % (session_id)
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s/1" % (session_id),
            json={
                "pricerange": {
                    "min": 10000,
                    "max": 20000
                }
            }
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s/1" % (str(uuid4()))
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204
