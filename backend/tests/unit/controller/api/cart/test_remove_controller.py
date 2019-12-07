import pytest
from flask import json

from backend.service import CartService
from backend.util.response.error import ErrorSchema
from backend.errors.request_error import ValidationError


@pytest.fixture(scope="function", autouse=True)
def controller_mocker(mocker):
    mocker.patch.object(CartService, "__init__", return_value=None)


def test_remove_controller(mocker, login_disabled_app, willstores_ws):
    mocker.patch.object(CartService, "remove_item", return_value=True)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/cart/remove/test"
        )

        data = json.loads(response.data)
        assert response.status_code == 200
        assert data == {}


def test_remove_controller_unregistered(mocker, login_disabled_app, willstores_ws):
    mocker.patch.object(CartService, "remove_item", side_effect=ValidationError("test"))

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/cart/remove/test"
        )

        data = json.loads(response.data)
        ErrorSchema().load(data)
        assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("remove_item", "POST", "api/cart/remove/test", Exception(), 500)
    ]
)
def test_remove_controller_error(mocker, willstores_ws, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(CartService, method, side_effect=error)

    make_request = get_request_function(http_method)

    response = make_request(
        test_url
    )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == status_code
