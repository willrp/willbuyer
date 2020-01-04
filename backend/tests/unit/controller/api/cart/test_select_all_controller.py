import pytest
import responses
import re
from flask import json
from json import JSONDecodeError
from werkzeug.exceptions import HTTPException
from requests import ConnectionError

from backend.service import CartService
from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="function", autouse=True)
def controller_mocker(mocker):
    mocker.patch.object(CartService, "__init__", return_value=None)


@pytest.fixture(scope="module")
def response_json():
    return {
        "total": {
            "outlet": 10.55,
            "retail": 20.9,
            "symbol": "£"
        },
        "products": [
            {
                "id": "id",
                "name": "string",
                "image": "string",
                "price": {
                    "outlet": 10.55,
                    "retail": 20.9,
                    "symbol": "£"
                },
                "discount": 80.5,
                "amount": 1
            }
        ]
    }


def test_select_all_controller(mocker, flask_app, willstores_ws, response_json):
    mocker.patch.object(CartService, "to_list", return_value=[{"item_id": "id", "amount": 1}])

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

        with flask_app.test_client() as client:
            response = client.get(
                "api/cart"
            )

            data = json.loads(response.data)
            CartSchema().load(data)
            assert response.status_code == 200


def test_select_all_controller_empty(mocker, flask_app):
    mocker.patch.object(CartService, "to_list", return_value=[])

    with flask_app.test_client() as client:
        response = client.get(
            "api/cart"
        )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("to_list", "GET", "api/cart", HTTPException(), 400),
        ("to_list", "GET", "api/cart", ConnectionError(), 502),
        ("to_list", "GET", "api/cart", Exception(), 500)
    ]
)
def test_select_by_slug_controller_error(mocker, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(CartService, method, side_effect=error)

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
        ("api/cart", 400),
        ("api/cart", 401),
        ("api/cart", 500),
        ("api/cart", 504),
    ]
)
def test_update_controller_http_error(mocker, flask_app, willstores_ws, json_error_recv, test_url, status_code):
    mocker.patch.object(CartService, "to_list", return_value=[{"item_id": "id", "amount": 1}])

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
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
