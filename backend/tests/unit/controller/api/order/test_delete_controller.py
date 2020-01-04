import pytest
import responses
import re
from flask import json
from unittest.mock import MagicMock

from backend.util.response.error import ErrorSchema


def test_delete_controller(mocker, login_disabled_app, willorders_ws):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.DELETE, re.compile(willorders_ws),
            status=200,
            json={}
        )

        with login_disabled_app.test_client() as client:
            response = client.delete(
                "api/order/delete/WILLrogerPEREIRAslugBR"
            )

            data = json.loads(response.data)
            assert data == {}
            assert response.status_code == 200


@pytest.mark.parametrize(
    "test_url, status_code",
    [
        ("api/order/delete/WILLrogerPEREIRAslugBR", 400),
        ("api/order/delete/WILLrogerPEREIRAslugBR", 401),
        ("api/order/delete/WILLrogerPEREIRAslugBR", 404),
        ("api/order/delete/WILLrogerPEREIRAslugBR", 500),
        ("api/order/delete/WILLrogerPEREIRAslugBR", 502),
        ("api/order/delete/WILLrogerPEREIRAslugBR", 504),
    ]
)
def test_select_by_slug_controller_http_error(mocker, login_disabled_app, willorders_ws, json_error_recv, test_url, status_code):
    mocker.patch("flask_login.utils._get_user", return_value=MagicMock(uuid_slug="test"))

    with responses.RequestsMock() as rsps:
        rsps.add(responses.DELETE, re.compile(willorders_ws),
            status=status_code,
            json=json_error_recv
        )

        with login_disabled_app.test_client() as client:
            response = client.delete(
                test_url
            )

        data = json.loads(response.data)
        ErrorSchema().load(data)

        assert response.status_code == status_code
