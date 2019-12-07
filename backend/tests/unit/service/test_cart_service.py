import pytest
from flask import session
from uuid import uuid4

from backend.service import CartService
from backend.errors.no_content_error import NoContentError
from backend.errors.request_error import ValidationError


@pytest.fixture(scope="function")
def service():
    service = CartService()
    return service


def test_cart_service_update_item(service, flask_app):
    item_id = str(uuid4())

    with flask_app.test_request_context():
        result = service.update_item(item_id, 1)

        assert result is True
        assert service.to_dict()[item_id] == 1

        result = service.update_item(item_id, 3)

        assert result is True
        assert service.to_dict()[item_id] == 3


def test_cart_service_remove_item(service, flask_app):
    item_id = str(uuid4())

    with flask_app.test_request_context():
        service.update_item(item_id, 1)

        assert service.to_dict()[item_id] == 1

        result = service.remove_item(item_id)

        assert result is True
        assert item_id not in service.to_dict()
        assert service.to_dict() == {}

        with pytest.raises(NoContentError):
            assert service.to_list() == []


def test_cart_service_remove_item_unregistered(service, flask_app):
    with flask_app.test_request_context():
        with pytest.raises(ValidationError):
            service.remove_item("test")


def test_cart_service_empty(service, flask_app):
    item_id = str(uuid4())
    item_id2 = str(uuid4())

    with flask_app.test_request_context():
        assert "cart" not in session

        service.empty()

        assert session["cart"] == {}

        service.update_item(item_id, 1)
        service.update_item(item_id2, 2)

        assert session["cart"] != {}

        service.empty()

        assert session["cart"] == {}


def test_cart_service_to_dict(service, flask_app):
    item_id = str(uuid4())
    item_id2 = str(uuid4())

    with flask_app.test_request_context():
        service.update_item(item_id, 1)
        service.update_item(item_id2, 2)
        result = service.to_dict()

        for key in [item_id, item_id2]:
            assert key in result

        assert result[item_id] == 1
        assert result[item_id2] == 2


def test_cart_service_to_dict_empty(service, flask_app):
    with flask_app.test_request_context():
        session["cart"] = dict()

        assert service.to_dict() == {}


def test_cart_service_to_dict_non_initialized(service, flask_app):
    with flask_app.test_request_context():
        assert service.to_dict() == {}


def test_cart_service_to_list(service, flask_app):
    item_id = str(uuid4())
    item_id2 = str(uuid4())

    with flask_app.test_request_context():
        service.update_item(item_id, 1)
        service.update_item(item_id2, 2)
        result = service.to_list()

        for item in result:
            assert item["item_id"] in [item_id, item_id2]
            assert item["amount"] in [1, 2]


def test_cart_service_to_list_empty(service, flask_app):
    with flask_app.test_request_context():
        session["cart"] = dict()

        with pytest.raises(NoContentError):
            assert service.to_list() == []


def test_cart_service_to_list_non_initialized(service, flask_app):
    with flask_app.test_request_context():
        with pytest.raises(NoContentError):
            assert service.to_list() == []
