def test_basic_front_end(flask_app):
    with flask_app.test_client() as client:
        response = client.get(
            "/a/random/page"
        )

    assert response.status_code == 200


def test_basic_front_end_next(flask_app, auth_user):
    with flask_app.test_client(user=auth_user) as client:
        with client.session_transaction() as sess:
            sess["next_url"] = "/another/random/page"

        response = client.get(
            "/a/random/page"
        )

    assert response.status_code == 302


def test_basic_front_end_next_unauthorized(flask_app):
    with flask_app.test_client() as client:
        with client.session_transaction() as sess:
            sess["next_url"] = "/another/random/page"

        response = client.get(
            "/a/random/page"
        )

    assert response.status_code == 200
