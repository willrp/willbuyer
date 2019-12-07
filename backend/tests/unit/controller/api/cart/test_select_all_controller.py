import pytest
from flask import json
from json import JSONDecodeError

from backend.service import CartService
from backend.util.response.cart import CartSchema
from backend.util.response.error import ErrorSchema
from backend.errors.no_content_error import NoContentError


@pytest.fixture(scope="function", autouse=True)
def controller_mocker(mocker):
    mocker.patch.object(CartService, "__init__", return_value=None)


def test_select_all_controller(mocker, login_disabled_app, willstores_ws):
    mocker.patch.object(CartService, "to_list", return_value=[{"item_id": "test", "amount": 1}])

    with login_disabled_app.test_client() as client:
        response = client.get(
            "api/cart"
        )

        data = json.loads(response.data)
        CartSchema().load(data)
        assert response.status_code == 200


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("to_list", "GET", "api/cart", NoContentError(), 204),
        ("to_list", "GET", "api/cart", Exception(), 500)
    ]
)
def test_select_by_slug_controller_error(mocker, willstores_ws, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(CartService, method, side_effect=error)

    make_request = get_request_function(http_method)

    response = make_request(
        test_url
    )

    if status_code == 204:
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)
    else:
        data = json.loads(response.data)
        ErrorSchema().load(data)

    assert response.status_code == status_code
