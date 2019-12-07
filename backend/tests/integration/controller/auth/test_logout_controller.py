from flask_login import current_user

from backend.controller.auth.login import user_logged_in
from backend.model import User, OAuth


def test_logout_controller(flask_app, db_perm_session, test_vcr, auth_user, auth_blueprint):
    assert len(db_perm_session.query(User).all()) == 1
    assert len(db_perm_session.query(OAuth).all()) == 1

    with flask_app.test_request_context("/auth/logout"):
        user_logged_in(auth_blueprint, auth_user.oauth.token)
        assert current_user.is_authenticated is True

        with flask_app.test_client(user=auth_user) as client:
            assert current_user.is_authenticated is True

            with test_vcr.use_cassette("auth_google_token_revoke.yml"):
                response = client.get(
                    "/auth/logout"
                )

                assert current_user.is_authenticated is False

        assert response.status_code == 302
        assert len(db_perm_session.query(User).all()) == 1
        assert len(db_perm_session.query(OAuth).all()) == 0
