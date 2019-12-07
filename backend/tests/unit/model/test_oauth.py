import pytest
from uuid import uuid4
from sqlalchemy.exc import IntegrityError

from backend.tests.factories import OAuthFactory, UserFactory


@pytest.fixture(scope="function", autouse=True)
def factory_session(db_session):
    OAuthFactory._meta.sqlalchemy_session = db_session
    UserFactory._meta.sqlalchemy_session = db_session


def test_oauth_insert_without_user(db_session):
    with pytest.raises(IntegrityError):
        OAuthFactory.create()
        db_session.commit()


def test_user_insert_same_uuid(db_session):
    test_uuid = uuid4()

    with pytest.raises(IntegrityError):
        test_user = UserFactory()
        test_oauth = OAuthFactory.create(uuid=test_uuid)
        test_oauth.user = test_user
        db_session.commit()
        test_user_2 = UserFactory()
        test_oauth_2 = OAuthFactory.create(uuid=test_uuid)
        test_oauth_2.user = test_user_2
        db_session.commit()


def test_oauth_insert_same_provider_user_id(db_session):
    with pytest.raises(IntegrityError):
        test_user = UserFactory()
        test_oauth = OAuthFactory.create(provider_user_id="1")
        test_oauth.user = test_user
        db_session.commit()
        test_user_2 = UserFactory()
        test_oauth_2 = OAuthFactory.create(provider_user_id="1")
        test_oauth_2.user = test_user_2
        db_session.commit()


def test_oauth_insert_oauth_same_user(db_session):
    with pytest.raises(IntegrityError):
        test_user = UserFactory()
        test_oauth = OAuthFactory.create()
        test_oauth.user = test_user
        db_session.commit()
        test_oauth_2 = OAuthFactory.create(provider_user_id="1")
        test_oauth_2.user = test_user
        db_session.commit()
