import pytest
import responses
import re
from flask import json
from unittest.mock import MagicMock
from copy import deepcopy
from json.decoder import JSONDecodeError
from requests import ConnectionError

from backend.util.request.order.user_orders import UserOrdersRequest
from backend.util.response.order.user_orders import UserOrdersSchema
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="module")
def request_json():
    return {
        "page": "1",
        "page_size": "5",
        "datespan": {
            "start": "2019-10-20",
            "end": "2019-10-24"
        }
    }


@pytest.fixture(scope="module")
def response_json():
    return {
        "orders": [
            {
                "slug": "slug",
                "user_slug": "user_slug",
                "product_types": 0,
                "items_amount": 0,
                "total": {
                    "outlet": 10.55,
                    "retail": 20.9,
                    "symbol": "£"
                },
                "updated_at": "2019-12-05T03:48:14.137Z"
            }
        ],
        "total": 0,
        "pages": 0
    }


def test_select_from_user_slug_controller(mocker, login_disabled_app, willorders_ws, request_json, response_json):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willorders_ws),
            status=200,
            json=response_json
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/order/user"
            )

        data = json.loads(response.data)
        UserOrdersSchema().load(data)
        assert response.status_code == 200
        assert len(data["orders"]) == 1
        assert data["total"] == 0
        assert data["pages"] == 0

        for order in data["orders"]:
            assert order["slug"] == "slug"
            assert order["user_slug"] == "user_slug"
            assert order["product_types"] == 0
            assert order["items_amount"] == 0
            assert order["total"]["outlet"] == 10.55
            assert order["total"]["retail"] == 20.9
            assert order["total"]["symbol"] == "£"


def test_select_from_user_slug_controller_no_content(mocker, login_disabled_app, willorders_ws):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willorders_ws),
            status=204
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                "api/order/user"
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)


def test_select_from_user_slug_controller_invalid_json(login_disabled_app, request_json):
    invalid_page = deepcopy(request_json)
    invalid_page.update(page=-1)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/order/user",
            json=invalid_page
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == 400

    toosmall_page_size = deepcopy(request_json)
    toosmall_page_size.update(page_size=0)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/order/user",
            json=toosmall_page_size
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == 400

    toobig_page_size = deepcopy(request_json)
    toobig_page_size.update(page_size=999)

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/order/user",
            json=toobig_page_size
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == 400

    switched_datespan = deepcopy(request_json)
    switched_datespan.update(datespan={"start": "2019-10-25", "end": "2019-10-23"})   

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/order/user",
            json=switched_datespan
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == 400

    overflow_datespan = deepcopy(request_json)
    overflow_datespan.update(datespan={"start": "2019-13-20", "end": "2019-10-33"})

    with login_disabled_app.test_client() as client:
        response = client.post(
            "api/order/user",
            json=overflow_datespan
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("parse_json", "POST", "api/order/user", ConnectionError(), 502),
        ("parse_json", "POST", "api/order/user", Exception(), 500)
    ]
)
def test_select_from_user_slug_controller_error(mocker, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(UserOrdersRequest, method, side_effect=error)
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
        ("api/order/user", 400),
        ("api/order/user", 401),
        ("api/order/user", 500),
        ("api/order/user", 502),
        ("api/order/user", 504),
    ]
)
def test_select_from_user_slug_controller_http_error(mocker, login_disabled_app, willorders_ws, json_error_recv, test_url, status_code):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willorders_ws),
            status=status_code,
            json=json_error_recv
        )

        with login_disabled_app.test_client() as client:
            response = client.post(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)

        assert response.status_code == status_code
