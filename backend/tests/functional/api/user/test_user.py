import requests

from backend.util.response.user import UserSchema
from backend.util.response.error import ErrorSchema


def test_user_current(domain_url, auth_session, auth_user):
    with auth_session as sess:
        response = sess.get(
            domain_url + "/api/user/current"
        )

    data = response.json()
    UserSchema().load(data)

    assert response.status_code == 200
    assert data == auth_user.to_dict()


def test_user_current_unauthorized(domain_url):
    response = requests.get(
        domain_url + "/api/user/current",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
