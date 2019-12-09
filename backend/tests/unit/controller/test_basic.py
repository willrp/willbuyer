def test_basic_front_end(flask_app):
    with flask_app.test_client() as client:
        response = client.get(
            "/a/random/page"
        )

    assert response.status_code == 200


def test_swagger_api(flask_app):
    with flask_app.test_client() as client:
        response = client.get(
            "/api/"
        )

    assert response.status_code == 200


def test_basic_front_end_next(flask_app):
    with flask_app.test_client() as client:
        response = client.get(
            "/a/random/page"
        )

    assert response.status_code == 200


def test_basic_front_end_wrong_method(flask_app):
    with flask_app.test_client() as client:
        response = client.put(
            "/go/index"
        )

    assert response.status_code == 405


def test_basic_api_wrong_method(flask_app):
    with flask_app.test_client() as client:
        response = client.patch(
            "/auth/"
        )

    assert response.status_code == 405
