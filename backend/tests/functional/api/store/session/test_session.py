import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.session_results import SessionResultsSchema
from backend.util.response.error import ErrorSchema
from backend.util.slug import uuid_to_slug


def test_session(domain_url, es_create, auth_session):
    session_list = es_create("sessions", 3, gender="Women")
    session_id = session_list[0].meta["id"]
    es_create("products", 5, gender="Women", sessionid=session_id)

    response = auth_session.post(
        domain_url + "/api/store/session/%s" % (session_id)
    )

    data = response.json()
    SessionResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 5

    response = auth_session.post(
        domain_url + "/api/store/session/%s" % (session_id),
        json={
            "pricerange": {
                "min": 1,
                "max": 500
            }
        }
    )

    data = response.json()
    SessionResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 5

    response = auth_session.post(
        domain_url + "/api/store/session/%s" % (session_id),
        json={
            "pricerange": {
                "min": 10000,
                "max": 20000
            }
        }
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    empty_session_id = session_list[1].meta["id"]

    response = auth_session.post(
        domain_url + "/api/store/session/%s" % (empty_session_id)
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    response = auth_session.post(
        domain_url + "/api/store/session/%s" % (uuid_to_slug(uuid4()))
    )

    assert response.status_code == 404


def test_session_unauthorized(domain_url):
    response = requests.post(
        domain_url + "/api/store/session/test",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
