import pytest
import responses
import re
from flask import json
from copy import deepcopy
from json.decoder import JSONDecodeError
from requests import ConnectionError

from backend.util.request.store.search_products_request import SearchProductsRequest
from backend.util.response.store.search_products_results import SearchProductsResultsSchema
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="module")
def request_json():
    return {
        "pricerange": {
            "min": 1000,
            "max": 2000
        },
        "pagesize": 5
    }


@pytest.fixture(scope="module")
def response_json():
    return {
        "products": [
            {
                "id": "string",
                "name": "string",
                "image": "string",
                "price": {
                    "outlet": 10.55,
                    "retail": 20.9,
                    "symbol": "£"
                },
                "discount": 80.5
            }
        ]
    }


def test_session_products_controller(login_disabled_app, willstores_ws, request_json, response_json):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test/1"
            )

        data = json.loads(response.data)
        SearchProductsResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["products"]) == 1

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test/1",
                json=request_json
            )

        data = json.loads(response.data)
        SearchProductsResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["products"]) == 1


def test_session_products_controller_no_content(login_disabled_app, willstores_ws, request_json):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=204
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test/1"
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/store/session/test/1",
                json=request_json
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)


def test_session_products_controller_invalid_page(login_disabled_app):
    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test/0"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400


def test_session_products_controller_invalid_json(mocker, login_disabled_app, request_json):
    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test/1",
            json="notjson"
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_min = deepcopy(request_json)
    invalid_min["pricerange"].update(min=-10.0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test/1",
            json=invalid_min
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_max = deepcopy(request_json)
    invalid_max["pricerange"].update(max=-10.0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test/1",
            json=invalid_max
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_range = deepcopy(request_json)
    invalid_range["pricerange"].update(min=100.0, max=50.0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test/1",
            json=invalid_range
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_pagesize = deepcopy(request_json)
    invalid_pagesize.update(pagesize=0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/store/session/test/1",
            json=invalid_pagesize
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("parse_json", "POST", "/api/store/session/test/1", ConnectionError(), 502),
        ("parse_json", "POST", "/api/store/session/test/1", Exception(), 500)
    ]
)
def test_session_products_controller_error(mocker, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(SearchProductsRequest, method, side_effect=error)
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
        ("/api/store/session/test/1", 204),
        ("/api/store/session/test/1", 400),
        ("/api/store/session/test/1", 401),
        ("/api/store/session/test/1", 404),
        ("/api/store/session/test/1", 500),
        ("/api/store/session/test/1", 502),
        ("/api/store/session/test/1", 504)
    ]
)
def test_session_products_controller_http_error(mocker, login_disabled_app, willstores_ws, json_error_recv, test_url, status_code):
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
