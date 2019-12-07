import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.gender_results import GenderResultsSchema
from backend.util.response.error import ErrorSchema


def test_gender(domain_url, es_create, auth_session):
    session_list = es_create("sessions", 3, gender="Women")
    session_id_0 = session_list[0].meta["id"]
    es_create("products", 3, gender="Women", sessionid=session_id_0)
    session_id_1 = session_list[1].meta["id"]
    es_create("products", 2, gender="Women", sessionid=session_id_1)

    response = auth_session.post(
        domain_url + "/api/store/gender/women"
    )

    data = response.json()
    GenderResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["discounts"]) >= 5

    response = auth_session.post(
        domain_url + "/api/store/gender/women",
        json={
            "amount": 1
        }
    )

    data = response.json()
    GenderResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["discounts"]) == 1

    response = auth_session.post(
        domain_url + "/api/store/gender/%s" % str(uuid4())
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204


def test_gender_unauthorized(domain_url):
    response = requests.post(
        domain_url + "/api/store/gender/women",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
