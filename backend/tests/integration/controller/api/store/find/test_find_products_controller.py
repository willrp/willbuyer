import pytest
from flask import json
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.search_products_results import SearchProductsResultsSchema
from backend.util.response.error import ErrorSchema


def test_find_products_controller(flask_app, es_create, auth_user):
    arg = str(uuid4())
    es_create("products", 5, brand=arg)
    es_create("products", 5, kind=arg)

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s/1" % (ftype, arg)
            )

        data = json.loads(response.data)
        SearchProductsResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["products"]) == 5

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s/1" % (arg)
        )

    data = json.loads(response.data)
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 10

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s/1" % (ftype, arg),
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

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s/1" % (arg),
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

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s/10" % (ftype, arg)
            )

        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        assert response.status_code == 204

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s/10" % (arg)
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s/1" % (ftype, arg),
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

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s/1" % (arg),
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

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s/1" % (ftype, str(uuid4()))
            )

        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        assert response.status_code == 204

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s/1" % (str(uuid4()))
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204


def test_find_products_controller_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.post(
            "api/store/find/brand/1/1",
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
