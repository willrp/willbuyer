import pytest
from uuid import uuid4
from sqlalchemy.exc import IntegrityError

from backend.model import User, OAuth
from backend.tests.factories import UserFactory, OAuthFactory


@pytest.fixture(scope="function", autouse=True)
def factory_session(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    OAuthFactory._meta.sqlalchemy_session = db_session


def test_user_select(db_session):
    assert db_session.query(User).one_or_none() is None

    UserFactory.create_batch(5)
    db_session.commit()

    assert len(db_session.query(User).all()) == 5


def test_user_insert(db_session):
    obj = UserFactory.create()
    db_session.commit()

    assert db_session.query(User).one()
    assert db_session.query(User).filter(User.id == obj.id).one()
    assert db_session.query(User).filter(User.uuid == obj.uuid).one()


def test_user_insert_oauth(db_session):
    user = UserFactory.create()
    oauth = OAuthFactory.create()
    oauth.user = user
    db_session.commit()

    assert db_session.query(User).one()
    assert db_session.query(OAuth).one()
    assert db_session.query(User).filter(User.oauth == oauth).one()


def test_user_insert_same_uuid(db_session):
    test_uuid = uuid4()
    with pytest.raises(IntegrityError):
        UserFactory.create(uuid=test_uuid)
        db_session.commit()
        UserFactory.create(uuid=test_uuid)
        db_session.commit()


def test_user_insert_same_provider_user_id(db_session):
    with pytest.raises(IntegrityError):
        UserFactory.create(provider_user_id="1")
        db_session.commit()
        UserFactory.create(provider_user_id="1")
        db_session.commit()


def test_user_update_oauth(db_session):
    user = UserFactory.create()
    db_session.commit()
    assert db_session.query(User).one()
    assert db_session.query(OAuth).one_or_none() is None

    oauth = OAuthFactory.create()
    oauth.user = user
    db_session.commit()
    assert db_session.query(User).one()
    assert db_session.query(OAuth).one()
    assert db_session.query(User).filter(User.oauth == oauth).one()

    result = db_session.query(OAuth).filter(OAuth.id == oauth.id).delete()
    db_session.commit()
    assert result == 1
    assert db_session.query(User).one()
    assert db_session.query(User).one().oauth is None
    assert db_session.query(OAuth).one_or_none() is None


def test_user_update_same_provider_user_id(db_session):
    UserFactory.create(provider_user_id="1")
    obj = UserFactory.create(provider_user_id="2")
    db_session.commit()

    with pytest.raises(IntegrityError):
        obj.provider_user_id = "1"
        db_session.commit()


def test_user_single_parent_constraint(db_session):
    obj = UserFactory.create()
    obj2 = UserFactory.create()

    assert obj.oauth is None
    assert obj2.oauth is None

    test_oauth = OAuthFactory.create()
    obj.oauth = test_oauth
    db_session.commit()

    assert obj.oauth is not None
    assert obj2.oauth is None

    res = obj.oauth
    obj2.oauth = res
    db_session.commit()

    assert obj.oauth is None
    assert obj2.oauth is not None
    assert obj2.oauth == res


def test_user_delete(db_session):
    obj = UserFactory.create()
    obj.oauth = OAuthFactory.create()
    db_session.commit()

    assert db_session.query(User).one()
    assert db_session.query(OAuth).one()

    result = db_session.query(User).filter(User.id == obj.id).delete()
    assert result == 1
    db_session.commit()

    assert db_session.query(User).one_or_none() is None
    assert db_session.query(OAuth).one_or_none() is None


def test_user_delete_non_existant(db_session):
    result = db_session.query(User).filter(User.id == 1).delete()
    db_session.commit()

    assert result == 0


def test_user_dict(db_session):
    obj = UserFactory.create()
    db_session.commit()
    obj_dict = obj.to_dict()
    assert len(obj_dict.keys()) == 3
    for key in ["name", "email", "picture"]:
        assert key in obj_dict
