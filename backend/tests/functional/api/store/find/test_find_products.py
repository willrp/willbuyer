import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.search_products_results import SearchProductsResultsSchema
from backend.util.response.error import ErrorSchema


def test_find_products(domain_url, es_create, auth_session):
    arg = str(uuid4())
    es_create("products", 5, brand=arg)
    es_create("products", 5, kind=arg)

    for ftype in ["brand", "kind"]:
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, arg)
        )

        data = response.json()
        SearchProductsResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["products"]) == 5

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s/1" % (arg)
    )

    data = response.json()
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 10

    for ftype in ["brand", "kind"]:        
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, arg),
            json={
                "pricerange": {
                    "min": 1,
                    "max": 500
                },
                "pagesize": 1
            }
        )

        data = response.json()
        SearchProductsResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["products"]) == 1

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s/1" % (arg),
        json={
            "pricerange": {
                "min": 1,
                "max": 500
            },
            "pagesize": 1
        }
    )

    data = response.json()
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 1

    for ftype in ["brand", "kind"]:
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s/10" % (ftype, arg)
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s/10" % (arg)
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    for ftype in ["brand", "kind"]:
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, arg),
            json={
                "pricerange": {
                    "min": 10000,
                    "max": 20000
                }
            }
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s/1" % (arg),
        json={
            "pricerange": {
                "min": 10000,
                "max": 20000
            }
        }
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    for ftype in ["brand", "kind"]:
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, str(uuid4()))
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s/1" % (str(uuid4()))
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204


def test_find_products_unauthorized(domain_url):
    response = requests.post(
        domain_url + "/api/store/find/brand/1/1",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
