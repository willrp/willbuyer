import pytest
from flask import json
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.search_results import SearchResultsSchema
from backend.util.response.error import ErrorSchema


def test_find_controller(flask_app, es_create, auth_user):
    arg = str(uuid4())
    es_create("products", 5, brand=arg)
    es_create("products", 5, kind=arg)

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s" % (ftype, arg)
            )

        data = json.loads(response.data)
        SearchResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 5

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s" % (arg)
        )

    data = json.loads(response.data)
    SearchResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 10

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s" % (ftype, arg),
                json={
                    "pricerange": {
                        "min": 1,
                        "max": 500
                    }
                }
            )

        data = json.loads(response.data)
        SearchResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 5

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s" % (arg),
            json={
                "pricerange": {
                    "min": 1,
                    "max": 500
                }
            }
        )

    data = json.loads(response.data)
    SearchResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 10

    for ftype in ["brand", "kind"]:
        with flask_app.test_client(user=auth_user) as client:
            response = client.post(
                "api/store/find/%s/%s" % (ftype, arg),
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
            "api/store/find/search/%s" % (arg),
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
                "api/store/find/%s/%s" % (ftype, str(uuid4()))
            )

        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        assert response.status_code == 204

    with flask_app.test_client(user=auth_user) as client:
        response = client.post(
            "api/store/find/search/%s" % (str(uuid4()))
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204


def test_find_controller_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.post(
            "api/store/find/search/1",
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
