import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.search_results import SearchResultsSchema
from backend.util.response.error import ErrorSchema


def test_find(domain_url, es_create, auth_session):
    arg = str(uuid4())
    es_create("products", 5, brand=arg)
    es_create("products", 5, kind=arg)

    for ftype in ["brand", "kind"]:
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s" % (ftype, arg)
        )

        data = response.json()
        SearchResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 5

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s" % (arg)
    )

    data = response.json()
    SearchResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 10

    for ftype in ["brand", "kind"]:
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s" % (ftype, arg),
            json={
                "pricerange": {
                    "min": 1,
                    "max": 500
                }
            }
        )

        data = response.json()
        SearchResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 5

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s" % (arg),
        json={
            "pricerange": {
                "min": 1,
                "max": 500
            }
        }
    )

    data = response.json()
    SearchResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 10

    for ftype in ["brand", "kind"]:
        response = auth_session.post(
            domain_url + "/api/store/find/%s/%s" % (ftype, arg),
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
        domain_url + "/api/store/find/search/%s" % (arg),
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
            domain_url + "/api/store/find/%s/%s" % (ftype, str(uuid4()))
        )

        with pytest.raises(JSONDecodeError):
            response.json()

        assert response.status_code == 204

    response = auth_session.post(
        domain_url + "/api/store/find/search/%s" % (str(uuid4()))
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204


def test_find_unauthorized(domain_url):
    response = requests.post(
        domain_url + "/api/store/find/search/1",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
