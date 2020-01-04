import pytest
import responses
import re
from flask import json
from copy import deepcopy
from json.decoder import JSONDecodeError
from requests import ConnectionError

from backend.util.request.store.gender_request import GenderRequest
from backend.util.response.store.gender_results import GenderResultsSchema
from backend.util.response.error import ErrorSchema


@pytest.fixture(scope="module")
def request_json():
    return {
        "amount": "5"
    }


@pytest.fixture(scope="module")
def response_json():
    return {
        "discounts": [
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
        ],
        "sessions": [
            {
                "id": "string",
                "name": "string",
                "gender": "string",
                "image": "string",
                "total": 100
            }
        ],
        "brands": [
            {
                "brand": "string",
                "amount": 10
            }
        ],
        "kinds": [
            {
                "kind": "string",
                "amount": 10
            }
        ]
    }


def test_gender_controller(flask_app, willstores_ws, request_json, response_json):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=200,
            json=response_json
        )

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/gender/test"
            )

        data = json.loads(response.data)
        GenderResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["discounts"]) == 1

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/gender/test",
                json=request_json
            )

        data = json.loads(response.data)
        GenderResultsSchema().load(data)
        assert response.status_code == 200
        assert len(data["discounts"]) == 1


def test_gender_controller_no_content(flask_app, willstores_ws, request_json):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=204
        )

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/gender/test"
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)

        with flask_app.test_client() as client:
            response = client.post(
                "api/store/gender/test",
                json=request_json
            )

        assert response.status_code == 204
        with pytest.raises(JSONDecodeError):
            json.loads(response.data)


def test_gender_controller_invalid_json(flask_app, willstores_ws, request_json):
    with flask_app.test_client() as client:
        response = client.post(
            "api/store/gender/test",
            json="notjson"
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400

    invalid_amount = deepcopy(request_json)
    invalid_amount.update(amount=0)

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/gender/test",
            json=invalid_amount
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "method,http_method,test_url,error,status_code",
    [
        ("parse_json", "POST", "/api/store/gender/test", ConnectionError(), 502),
        ("parse_json", "POST", "/api/store/gender/test", Exception(), 500)
    ]
)
def test_gender_controller_error(mocker, get_request_function, method, http_method, test_url, error, status_code):
    mocker.patch.object(GenderRequest, method, side_effect=error)
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
        ("/api/store/gender/test", 204),
        ("/api/store/gender/test", 400),
        ("/api/store/gender/test", 401),
        ("/api/store/gender/test", 500),
        ("/api/store/gender/test", 502),
        ("/api/store/gender/test", 504)
    ]
)
def test_gender_controller_http_error(flask_app, willstores_ws, json_error_recv, test_url, status_code):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, re.compile(willstores_ws),
            status=status_code,
            json=json_error_recv
        )

        with flask_app.test_client() as client:
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
