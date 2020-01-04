import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.session_results import SessionResultsSchema
from backend.util.slug import uuid_to_slug


def test_session(domain_url, es_create):
    session_list = es_create("sessions", 3, gender="Women")
    session_id = session_list[0].meta["id"]
    es_create("products", 5, gender="Women", sessionid=session_id)

    response = requests.post(
        domain_url + "/api/store/session/%s" % (session_id),
        verify=False
    )

    data = response.json()
    SessionResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 5

    response = requests.post(
        domain_url + "/api/store/session/%s" % (session_id),
        json={
            "pricerange": {
                "min": 1,
                "max": 500
            }
        },
        verify=False
    )

    data = response.json()
    SessionResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 5

    response = requests.post(
        domain_url + "/api/store/session/%s" % (session_id),
        json={
            "pricerange": {
                "min": 10000,
                "max": 20000
            }
        },
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    empty_session_id = session_list[1].meta["id"]

    response = requests.post(
        domain_url + "/api/store/session/%s" % (empty_session_id),
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204

    response = requests.post(
        domain_url + "/api/store/session/%s" % (uuid_to_slug(uuid4())),
        verify=False
    )

    assert response.status_code == 404
