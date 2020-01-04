import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.search_products_results import SearchProductsResultsSchema


def test_find_products(domain_url, es_create):
    arg = str(uuid4())
    es_create("products", 5, brand=arg)
    es_create("products", 5, kind=arg)

    for ftype in ["brand", "kind"]:
        response = requests.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, arg),
            verify=False
        )

        data = response.json()
        SearchProductsResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["products"]) == 5

    response = requests.post(
        domain_url + "/api/store/find/search/%s/1" % (arg),
        verify=False
    )

    data = response.json()
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 10

    for ftype in ["brand", "kind"]:        
        response = requests.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, arg),
            json={
                "pricerange": {
                    "min": 1,
                    "max": 500
                },
                "pagesize": 1
            },
            verify=False
        )

        data = response.json()
        SearchProductsResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["products"]) == 1

    response = requests.post(
        domain_url + "/api/store/find/search/%s/1" % (arg),
        json={
            "pricerange": {
                "min": 1,
                "max": 500
            },
            "pagesize": 1
        },
        verify=False
    )

    data = response.json()
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 1

    for ftype in ["brand", "kind"]:
        response = requests.post(
            domain_url + "/api/store/find/%s/%s/10" % (ftype, arg),
            verify=False
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

    response = requests.post(
        domain_url + "/api/store/find/search/%s/10" % (arg),
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    for ftype in ["brand", "kind"]:
        response = requests.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, arg),
            json={
                "pricerange": {
                    "min": 10000,
                    "max": 20000
                }
            },
            verify=False
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

    response = requests.post(
        domain_url + "/api/store/find/search/%s/1" % (arg),
        json={
            "pricerange": {
                "min": 10000,
                "max": 20000
            }
        },
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    for ftype in ["brand", "kind"]:
        response = requests.post(
            domain_url + "/api/store/find/%s/%s/1" % (ftype, str(uuid4())),
            verify=False
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

    response = requests.post(
        domain_url + "/api/store/find/search/%s/1" % (str(uuid4())),
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204
