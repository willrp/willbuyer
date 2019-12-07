import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import DatabaseError

from backend.service import UserService


@pytest.fixture(scope="function", autouse=True)
def service_mocker(mocker, service_init_mock):
    mocker.patch("backend.service.UserService.__init__", new=service_init_mock)


@pytest.fixture(scope="function")
def service():
    service = UserService()
    return service


def test_user_service_get_create_oauth_creates(service):
    service.db_session.query().filter_by().one_or_none.return_value = None
    obj = service.get_create_oauth(provider="provider", provider_user_id="1", token={})
    assert obj.provider == "provider"
    assert obj.provider_user_id == "1"


def test_user_service_get_create_oauth_gets(service):
    service.db_session.query().filter_by().one_or_none.return_value = MagicMock(autospec=True, provider="provider", provider_user_id="1")
    obj = service.get_create_oauth(provider="provider", provider_user_id="1", token={})
    assert obj.provider == "provider"
    assert obj.provider_user_id == "1"


def test_user_service_get_create_user_creates(service):
    service.db_session.query().filter_by().one_or_none.return_value = None
    obj = service.get_create_user(MagicMock(autospec=True), email="email", name="name", picture="picture")
    assert obj.name == "name"
    assert obj.picture == "picture"


def test_user_service_get_create_user_gets(service):
    service.db_session.query().filter_by().one_or_none.return_value = MagicMock(autospec=True, name="name", picture="picture")
    obj = service.get_create_user(MagicMock(autospec=True), email="email", name="new name", picture="new picture")
    assert obj.name == "new name"
    assert obj.picture == "new picture"


def test_user_service_get_create_user_error(service):
    service.db_session.query().filter_by().one_or_none.return_value = None
    service.db_session.add_all.side_effect = DatabaseError("statement", "params", "DETAIL:  orig\n")
    with pytest.raises(DatabaseError):
        service.get_create_user(MagicMock(autospec=True), email="email", name="new name", picture="new picture")
