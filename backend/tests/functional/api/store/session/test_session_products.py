import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.search_products_results import SearchProductsResultsSchema


def test_session_products(domain_url, es_create):
    session_list = es_create("sessions", 3, gender="Women")
    session_id = session_list[0].meta["id"]
    es_create("products", 5, gender="Women", sessionid=session_id)

    response = requests.post(
        domain_url + "/api/store/session/%s/1" % (session_id),
        verify=False
    )

    data = response.json()
    SearchProductsResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["products"]) == 5

    response = requests.post(
        domain_url + "/api/store/session/%s/1" % (session_id),
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
        domain_url + "/api/store/session/%s/10" % (session_id),
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    response = requests.post(
        domain_url + "/api/store/session/%s/1" % (session_id),
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
        domain_url + "/api/store/session/%s/1" % (str(uuid4())),
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204
