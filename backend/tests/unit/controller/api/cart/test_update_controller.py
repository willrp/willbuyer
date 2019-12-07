import pytest
import responses
import re
from flask import json, session
from werkzeug.exceptions import HTTPException
from requests import ConnectionError

from backend.service import CartService
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="function", autouse=True)
def controller_mocker(mocker):
    mocker.patch.object(CartService, "__init__", return_value=None)


def test_update_controller(mocker, login_disabled_app, willstores_ws):
    mocker.patch.object(CartService, "update_item", return_value=True)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willstores_ws),
            status=200,
            json={}
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/cart/update/test/1"
            )

            data = json.loads(response.data)
            assert response.status_code == 200
            assert data == {}


def test_update_controller_unregistered(login_disabled_app, willstores_ws):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willstores_ws),
            status=404,
            json={}
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/cart/update/test/1"
            )

            data = json.loads(response.data)
            ErrorSchema().load(data)
            assert response.status_code == 400
            assert "cart" not in session


def test_update_controller_invalid_amount(login_disabled_app):
    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/cart/update/test/0"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("update_item", "POST", "api/cart/update/test/1", HTTPException(), 400),
        ("update_item", "POST", "api/cart/update/test/1", ConnectionError(), 502),
        ("update_item", "POST", "api/cart/update/test/1", Exception(), 500)
    ]
)
def test_update_controller_error(mocker, willstores_ws, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(CartService, method, side_effect=error)

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willstores_ws),
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
        ("api/cart/update/test/1", 401),
        ("api/cart/update/test/1", 404),
        ("api/cart/update/test/1", 500),
        ("api/cart/update/test/1", 502),
        ("api/cart/update/test/1", 504),
    ]
)
def test_update_controller_http_error(login_disabled_app, willstores_ws, json_error_recv, test_url, status_code):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, re.compile(willstores_ws),
            status=status_code,
            json=json_error_recv
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)

        if status_code == 404:
            assert response.status_code == 400
        else:
            assert response.status_code == status_code
