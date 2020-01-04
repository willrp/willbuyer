import pytest
import responses
import re
from flask import json
from copy import deepcopy
from json.decoder import JSONDecodeError
from requests import ConnectionError

from backend.util.request.store.search_request import SearchRequest
from backend.util.response.store.search_results import SearchResultsSchema
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="module")
def request_json():
    return {
        "pricerange": {
            "min": 1000,
            "max": 2000
        }
    }


@pytest.fixture(scope="module")
def response_json():
    return {
        "total": 10,
        "pricerange": {
            "min": 10,
            "max": 20
        },
        "brands": [
            {
                "brand": "string",
                "amount": 10
            }
        ],
        "kinds": [
            {
                "kind": "string",
                "amount": 10
            }
        ]
    }


@pytest.mark.parametrize(
    "ftype",
    [
        ("brand"),
        ("kind"),
        ("search")
    ]
)
def test_find_controller(flask_app, willstores_ws, request_json, response_json, ftype):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/find/%s/test" % ftype
            )

        data = json.loads(response.data)
        SearchResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 10

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/find/%s/test" % ftype,
                json=request_json
            )

        data = json.loads(response.data)
        SearchResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 10


@pytest.mark.parametrize(
    "ftype",
    [
        ("brand"),
        ("kind"),
        ("search")
    ]
)
def test_find_controller_no_content(flask_app, willstores_ws, request_json, ftype):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=204
        )

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/find/%s/test" % ftype
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/find/%s/test" % ftype,
                json=request_json
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)


def test_find_controller_invalid_ftype(flask_app):
    with flask_app.test_client() as client:
        response = client.post(
            "api/store/find/invalid/test"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400


@pytest.mark.parametrize(
    "ftype",
    [
        ("brand"),
        ("kind"),
        ("search")
    ]
)
def test_find_controller_invalid_json(flask_app, request_json, ftype):
    with flask_app.test_client() as client:
        response = client.post(
            "api/store/find/%s/test" % ftype,
            json="notjson"
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_min = deepcopy(request_json)
    invalid_min["pricerange"].update(min=-10.0)

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/find/%s/test" % ftype,
            json=invalid_min
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_max = deepcopy(request_json)
    invalid_max["pricerange"].update(max=-10.0)

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/find/%s/test" % ftype,
            json=invalid_max
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_range = deepcopy(request_json)
    invalid_range["pricerange"].update(min=100.0, max=50.0)

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/find/%s/test" % ftype,
            json=invalid_range
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("parse_json", "POST", "/api/store/find/brand/test", ConnectionError(), 502),
        ("parse_json", "POST", "/api/store/find/kind/test", ConnectionError(), 502),
        ("parse_json", "POST", "/api/store/find/search/test", ConnectionError(), 502),
        ("parse_json", "POST", "/api/store/find/brand/test", Exception(), 500),
        ("parse_json", "POST", "/api/store/find/kind/test", Exception(), 500),
        ("parse_json", "POST", "/api/store/find/search/test", Exception(), 500)
    ]
)
def test_find_controller_error(mocker, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(SearchRequest, method, side_effect=error)
    make_request = get_request_function(http_method)

    response = make_request(
        test_url
    )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "test_url, status_code",
    [
        ("/api/store/find/brand/test", 204),
        ("/api/store/find/kind/test", 204),
        ("/api/store/find/search/test", 204),
        ("/api/store/find/brand/test", 400),
        ("/api/store/find/kind/test", 400),
        ("/api/store/find/search/test", 400),
        ("/api/store/find/brand/test", 401),
        ("/api/store/find/kind/test", 401),
        ("/api/store/find/search/test", 401),
        ("/api/store/find/brand/test", 500),
        ("/api/store/find/kind/test", 500),
        ("/api/store/find/search/test", 500),
        ("/api/store/find/brand/test", 502),
        ("/api/store/find/kind/test", 502),
        ("/api/store/find/search/test", 502),
        ("/api/store/find/brand/test", 504),
        ("/api/store/find/kind/test", 504),
        ("/api/store/find/search/test", 504),
    ]
)
def test_find_controller_http_error(flask_app, willstores_ws, json_error_recv, test_url, status_code):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=status_code,
            json=json_error_recv
        )

        with flask_app.test_client() as client:
            response = client.post(
                test_url
            )

        if status_code == 204:
            with pytest.raises(JSONDecodeError):
                json.loads(response.data)
        else:
            data = json.loads(response.data)
            ErrorSchema().load(data)

        assert response.status_code == status_code
