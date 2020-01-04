import pytest
from flask import json
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.gender_results import GenderResultsSchema


def test_gender_controller(flask_app, es_create):
    session_list = es_create("sessions", 3, gender="Women")
    session_id_0 = session_list[0].meta["id"]
    es_create("products", 3, gender="Women", sessionid=session_id_0)
    session_id_1 = session_list[1].meta["id"]
    es_create("products", 2, gender="Women", sessionid=session_id_1)

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/gender/women"
        )

    data = json.loads(response.data)
    GenderResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["discounts"]) >= 5

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/gender/women",
            json={
                "amount": 1
            }
        )

    data = json.loads(response.data)
    GenderResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["discounts"]) == 1

    with flask_app.test_client() as client:
        response = client.post(
            "api/store/gender/%s" % str(uuid4())
        )

    with pytest.raises(JSONDecodeError):
        json.loads(response.data)

    assert response.status_code == 204
