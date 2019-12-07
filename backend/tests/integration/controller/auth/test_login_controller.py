from flask import session
from flask_login import current_user

from backend.controller.auth.login import user_logged_in
from backend.model import User, OAuth


def test_login_controller_create_user(flask_app, db_perm_session, auth_blueprint):
    assert len(db_perm_session.query(User).all()) == 0
    assert len(db_perm_session.query(OAuth).all()) == 0

    with flask_app.test_request_context("/auth/google/authorized"):
        assert current_user.is_authenticated is False
        returned = user_logged_in(auth_blueprint, auth_blueprint.session.token)
        logged_in_uid = session.get("user_id")
        assert current_user.is_authenticated is True

    assert returned is False
    assert len(db_perm_session.query(User).all()) == 1
    assert len(db_perm_session.query(OAuth).all()) == 1

    oauth = db_perm_session.query(OAuth).first()
    assert oauth.provider == "google"

    user = db_perm_session.query(User).first()
    assert logged_in_uid == str(user.id)


def test_login_controller_login_user(flask_app, db_perm_session, auth_user, auth_blueprint):
    assert len(db_perm_session.query(User).all()) == 1
    assert len(db_perm_session.query(OAuth).all()) == 1

    with flask_app.test_request_context("/auth/google/authorized"):
        assert current_user.is_authenticated is False
        returned = user_logged_in(auth_blueprint, auth_user.oauth.token)
        logged_in_uid = session.get("user_id")
        assert current_user.is_authenticated is True

    assert returned is False
    assert len(db_perm_session.query(User).all()) == 1
    assert len(db_perm_session.query(OAuth).all()) == 1
    assert logged_in_uid == str(auth_user.id)
