import pytest
import requests
from uuid import uuid4
from json.decoder import JSONDecodeError

from backend.util.response.store.gender_results import GenderResultsSchema


def test_gender(domain_url, es_create):
    session_list = es_create("sessions", 3, gender="Women")
    session_id_0 = session_list[0].meta["id"]
    es_create("products", 3, gender="Women", sessionid=session_id_0)
    session_id_1 = session_list[1].meta["id"]
    es_create("products", 2, gender="Women", sessionid=session_id_1)

    response = requests.post(
        domain_url + "/api/store/gender/women",
        verify=False
    )

    data = response.json()
    GenderResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["discounts"]) >= 5

    response = requests.post(
        domain_url + "/api/store/gender/women",
        json={
            "amount": 1
        },
        verify=False
    )

    data = response.json()
    GenderResultsSchema().load(data)
    assert response.status_code == 200
    assert len(data["discounts"]) == 1

    response = requests.post(
        domain_url + "/api/store/gender/%s" % str(uuid4()),
        verify=False
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204
