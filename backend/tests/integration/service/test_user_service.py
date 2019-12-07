import pytest

from backend.service import UserService
from backend.model import User, OAuth
from backend.tests.factories import UserFactory, OAuthFactory


@pytest.fixture(scope="function", autouse=True)
def factory_session(db_perm_session):
    UserFactory._meta.sqlalchemy_session = db_perm_session
    OAuthFactory._meta.sqlalchemy_session = db_perm_session


@pytest.fixture(scope="session")
def service():
    service = UserService()
    return service


def test_user_service_get_create_oauth(service, db_perm_session):
    assert len(service.db_session.query(User).all()) == 0
    assert len(service.db_session.query(OAuth).all()) == 0

    obj = service.get_create_oauth(provider="google", provider_user_id="test", token={})

    assert obj.provider_user_id == "test"
    assert obj.user is None

    test_user = UserFactory.create()
    obj = OAuthFactory.create()
    obj.user = test_user
    db_perm_session.commit()

    assert len(service.db_session.query(User).all()) == 1
    assert len(service.db_session.query(OAuth).all()) == 1

    obj = service.get_create_oauth(provider=test_user.oauth.provider, provider_user_id=test_user.oauth.provider_user_id, token={})

    assert obj.id == test_user.oauth.id
    assert obj.uuid == test_user.oauth.uuid
    assert obj.user == test_user


def test_user_service_get_create_user(service, db_perm_session):
    assert len(service.db_session.query(User).all()) == 0
    assert len(service.db_session.query(OAuth).all()) == 0

    test_oauth = service.get_create_oauth(provider="google", provider_user_id="1", token={})
    obj = service.get_create_user(oauth=test_oauth, email="email", name="name", picture="picture")

    assert obj.oauth == test_oauth
    assert len(service.db_session.query(User).all()) == 1
    assert len(service.db_session.query(OAuth).all()) == 1

    updated_obj = service.get_create_user(oauth=test_oauth, email="email", name="new name", picture="new picture")

    assert updated_obj.oauth == test_oauth
    assert updated_obj.name == "new name"
    assert updated_obj.picture == "new picture"
    assert len(service.db_session.query(User).all()) == 1
    assert len(service.db_session.query(OAuth).all()) == 1
