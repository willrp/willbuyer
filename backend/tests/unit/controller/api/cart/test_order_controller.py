import pytest
import responses
import re
from flask import json
from unittest.mock import MagicMock
from werkzeug.exceptions import HTTPException
from requests import ConnectionError

from backend.service import CartService
from backend.util.response.error import ErrorSchema
from backend.errors.no_content_error import NoContentError


@pytest.fixture(scope="function", autouse=True)
def controller_mocker(mocker):
    mocker.patch.object(CartService, "__init__", return_value=None)


def test_order_controller(mocker, login_disabled_app, willorders_ws):
    mocker.patch.object(CartService, "to_list", return_value=[{"item_id": "test", "amount": 1}])
    mocker.patch.object(CartService, "empty", return_value=True)
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT, re.compile(willorders_ws),
            status=200,
            json={}
        )

        with login_disabled_app.test_client() as client:
            response = client.put(
                "api/cart/order"
            )

            data = json.loads(response.data)
            assert response.status_code == 201
            assert data == {}


def test_order_controller_empty_cart(mocker, login_disabled_app):
    mocker.patch.object(CartService, "to_list", side_effect=NoContentError())

    with login_disabled_app.test_client() as client:
        response = client.put(
            "api/cart/order"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400



def test_order_controller_unregistered(mocker, login_disabled_app, willorders_ws):
    mocker.patch.object(CartService, "to_list", return_value=[{"item_id": "test", "amount": 1}])
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT, re.compile(willorders_ws),
            status=400,
            json={"error": "test"}
        )

        with login_disabled_app.test_client() as client:
            response = client.put(
                "api/cart/order"
            )

            data = json.loads(response.data)
            ErrorSchema().load(data)
            assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("to_list", "PUT", "api/cart/order", HTTPException(), 400),
        ("to_list", "PUT", "api/cart/order", ConnectionError(), 502),
        ("to_list", "PUT", "api/cart/order", Exception(), 500)
    ]
)
def test_order_controller_error(mocker, willorders_ws, get_request_function, method, http_method, test_url, error, status_code):
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
        ("api/cart/order", 400),
        ("api/cart/order", 401),
        ("api/cart/order", 500),
        ("api/cart/order", 502),
        ("api/cart/order", 504),
    ]
)
def test_order_controller_http_error(mocker, login_disabled_app, willorders_ws, json_error_recv, test_url, status_code):
    mocker.patch.object(CartService, "to_list", return_value=[{"item_id": "test", "amount": 1}])
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT, re.compile(willorders_ws),
            status=status_code,
            json=json_error_recv
        )

        with login_disabled_app.test_client() as client:
            response = client.put(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == status_code
