import pytest
import responses
import re
from flask import json, session
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


def test_update_controller(mocker, flask_app, willstores_ws, response_json):
    mocker.patch.object(CartService, "to_dict", return_value={})
    mocker.patch.object(CartService, "update_item", return_value=True)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

        with flask_app.test_client() as client:
            response = client.post(
                "api/cart/update/id/1"
            )

            data = json.loads(response.data)
            CartSchema().load(data)
            assert response.status_code == 200


def test_update_controller_unregistered(flask_app, willstores_ws, json_error_recv):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=400,
            json=json_error_recv
        )

        with flask_app.test_client() as client:
            response = client.post(
                "api/cart/update/id/1"
            )

            data = json.loads(response.data)
            ErrorSchema().load(data)
            assert response.status_code == 400
            assert "cart" not in session


def test_update_controller_invalid_amount(flask_app):
    with flask_app.test_client() as client:
        response = client.post(
            "api/cart/update/id/0"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("update_item", "POST", "api/cart/update/id/1", HTTPException(), 400),
        ("update_item", "POST", "api/cart/update/id/1", ConnectionError(), 502),
        ("update_item", "POST", "api/cart/update/id/1", Exception(), 500)
    ]
)
def test_update_controller_error(mocker, willstores_ws, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(CartService, method, side_effect=error)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=200,
            json={}
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
        ("api/cart/update/id/1", 400),
        ("api/cart/update/id/1", 401),
        ("api/cart/update/id/1", 500),
        ("api/cart/update/id/1", 502),
        ("api/cart/update/id/1", 504),
    ]
)
def test_update_controller_http_error(flask_app, willstores_ws, json_error_recv, test_url, status_code):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=status_code,
            json=json_error_recv
        )

        with flask_app.test_client() as client:
            response = client.post(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)

        assert response.status_code == status_code
