import pytest
from flask import json
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.session_results import SessionResultsSchema
from backend.util.slug import uuid_to_slug


def test_session_controller(flask_app, es_create):
    session_list = es_create("sessions", 3, gender="Women")
    session_id = session_list[0].meta["id"]
    es_create("products", 5, gender="Women", sessionid=session_id)

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s" % (session_id)
        )

    data = json.loads(response.data)
    SessionResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 5

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s" % (session_id),
            json={
                "pricerange": {
                    "min": 1,
                    "max": 500
                }
            }
        )

    data = json.loads(response.data)
    SessionResultsSchema().load(data)
    assert response.status_code == 200
    assert data["total"] == 5

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s" % (session_id),
            json={
                "pricerange": {
                    "min": 10000,
                    "max": 20000
                }
            }
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204

    empty_session_id = session_list[1].meta["id"]

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s" % (empty_session_id)
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/session/%s" % (uuid_to_slug(uuid4()))
        )

    assert response.status_code == 404
