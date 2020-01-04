import pytest
import responses
import re
from flask import json
from unittest.mock import MagicMock
from requests import ConnectionError

from backend.util.response.order.order import OrderSchema, OrderResponse
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="module")
def response_json():
    return {
        "slug": "slug",
        "product_types": 0,
        "items_amount": 0,
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
                "amount": 0
            }
        ],
        "updated_at": "2019-10-12T00:00:00.000Z"
    }


def test_select_by_slug_controller(mocker, login_disabled_app, willorders_ws, response_json):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willorders_ws),
            status=200,
            json=response_json
        )

        with login_disabled_app.test_client() as client:
            response = client.get(
                "api/order/WILLrogerPEREIRAslugBR"
            )

        data = json.loads(response.data)
        OrderSchema().load(data)
        assert response.status_code == 200
        assert data["slug"] == "slug"
        assert data["product_types"] == 0
        assert data["items_amount"] == 0
        assert len(data["products"]) == 1


def test_select_by_slug_controller_invalid_slug(mocker, login_disabled_app):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with login_disabled_app.test_client() as client:
        response = client.get(
            "api/order/invalidslug"
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("marshall_json", "GET", "api/order/WILLrogerPEREIRAslugBR", ConnectionError(), 502),
        ("marshall_json", "GET", "api/order/WILLrogerPEREIRAslugBR", Exception(), 500)
    ]
)
def test_select_by_slug_controller_error(mocker, willorders_ws, get_request_function, response_json, method, http_method, test_url, error, status_code):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))
    mocker.patch.object(OrderResponse, method, side_effect=error)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willorders_ws),
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
        ("api/order/WILLrogerPEREIRAslugBR", 400),
        ("api/order/WILLrogerPEREIRAslugBR", 401),
        ("api/order/WILLrogerPEREIRAslugBR", 404),
        ("api/order/WILLrogerPEREIRAslugBR", 500),
        ("api/order/WILLrogerPEREIRAslugBR", 502),
        ("api/order/WILLrogerPEREIRAslugBR", 504),
    ]
)
def test_select_by_slug_controller_http_error(mocker, login_disabled_app, willorders_ws, json_error_recv, test_url, status_code):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willorders_ws),
            status=status_code,
            json=json_error_recv
        )

        with login_disabled_app.test_client() as client:
            response = client.get(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)

        assert response.status_code == status_code
