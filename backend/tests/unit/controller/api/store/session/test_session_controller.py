import pytest
import responses
import re
from flask import json
from copy import deepcopy
from json.decoder import JSONDecodeError
from requests import ConnectionError

from backend.util.request.store.search_request import SearchRequest
from backend.util.response.store.session_results import SessionResultsSchema
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
        ],
        "sessions": [
            {
                "id": "string",
                "name": "string",
                "gender": "string",
                "image": "string",
                "total": 100
            }
        ]
    }


def test_session_controller(login_disabled_app, willstores_ws, request_json, response_json):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test"
            )

        data = json.loads(response.data)
        SessionResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 10

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test",
                json=request_json
            )

        data = json.loads(response.data)
        SessionResultsSchema().load(data)
        assert response.status_code == 200
        assert data["total"] == 10


def test_session_controller_no_content(login_disabled_app, willstores_ws, request_json):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=204
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test"
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test",
                json=request_json
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)


def test_session_controller_invalid_json(login_disabled_app, request_json):
    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test",
            json="notjson"
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_min = deepcopy(request_json)
    invalid_min["pricerange"].update(min=-10.0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test",
            json=invalid_min
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_max = deepcopy(request_json)
    invalid_max["pricerange"].update(max=-10.0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test",
            json=invalid_max
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_range = deepcopy(request_json)
    invalid_range["pricerange"].update(min=100.0, max=50.0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test",
            json=invalid_range
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("parse_json", "POST", "/api/store/session/test", ConnectionError(), 502),
        ("parse_json", "POST", "/api/store/session/test", Exception(), 500)
    ]
)
def test_session_controller_error(mocker, get_request_function, method, http_method, test_url, error, status_code):
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
        ("/api/store/session/test", 204),
        ("/api/store/session/test", 400),
        ("/api/store/session/test", 401),
        ("/api/store/session/test", 404),
        ("/api/store/session/test", 500),
        ("/api/store/session/test", 502),
        ("/api/store/session/test", 504)
    ]
)
def test_session_controller_http_error(login_disabled_app, willstores_ws, json_error_recv, test_url, status_code):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=status_code,
            json=json_error_recv
        )

        with login_disabled_app.test_client() as client:
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
