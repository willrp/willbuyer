import pytest
import responses
import re
from flask import json
from requests import ConnectionError

from backend.util.response.store.product_results import ProductResultsSchema, ProductResultsResponse
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="module")
def response_json():
    return {
        "id": "string",
        "name": "string",
        "kind": "string",
        "brand": "string",
        "details": [
            "string"
        ],
        "care": "string",
        "about": "string",
        "images": [
            "string"
        ],
        "gender": "string",
        "price": {
            "outlet": 10.55,
            "retail": 20.9,
            "symbol": "£"
        }
    }


def test_product_controller(flask_app, willstores_ws, response_json):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

        with flask_app.test_client() as client:
            response = client.get(
                "api/store/product/id"
            )

        data = json.loads(response.data)
        ProductResultsSchema().load(data)
        assert response.status_code == 200


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("marshall_json", "GET", "api/store/product/id", ConnectionError(), 502),
        ("marshall_json", "GET", "api/store/product/id", Exception(), 500)
    ]
)
def test_product_controller_error(mocker, willstores_ws, get_request_function, response_json, method, http_method, test_url, error, status_code):
    mocker.patch.object(ProductResultsResponse, method, side_effect=error)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

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
        ("api/store/product/id", 400),
        ("api/store/product/id", 401),
        ("api/store/product/id", 404),
        ("api/store/product/id", 500),
        ("api/store/product/id", 502),
        ("api/store/product/id", 504)
    ]
)
def test_product_controller_http_error(flask_app, willstores_ws, json_error_recv, test_url, status_code):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willstores_ws),
            status=status_code,
            json=json_error_recv
        )

        with flask_app.test_client() as client:
            response = client.get(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)

        assert response.status_code == status_code
