from backend.model import User, OAuth


def test_logout(domain_url, flask_app, db_perm_session, test_vcr, auth_session):
    assert len(db_perm_session.query(User).all()) == 1
    assert len(db_perm_session.query(OAuth).all()) == 1

    with test_vcr.use_cassette("auth_google_token_revoke.yml"):
        response = auth_session.get(
            domain_url + "/auth/logout",
            allow_redirects=False
        )

        assert response.status_code == 302
        assert len(db_perm_session.query(User).all()) == 1
        assert len(db_perm_session.query(OAuth).all()) == 0
