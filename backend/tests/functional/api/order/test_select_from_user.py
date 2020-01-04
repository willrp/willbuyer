import pytest
import requests
from datetime import date, timedelta
from json import JSONDecodeError

from backend.util.response.order.user_orders import UserOrdersSchema
from backend.util.response.error import ErrorSchema
from webservices.willorders.backend.tests.factories import OrderFactory, ProductFactory, OrderProductFactory


@pytest.fixture(scope="function", autouse=True)
def factory_session(willorders_ws_db_session):
    OrderFactory._meta.sqlalchemy_session = willorders_ws_db_session
    ProductFactory._meta.sqlalchemy_session = willorders_ws_db_session
    OrderProductFactory._meta.sqlalchemy_session = willorders_ws_db_session


def test_select_from_user(domain_url, auth_user, auth_session, es_create, willorders_ws_db_session):
    prod_list = es_create("products", 5)
    user_slug = auth_user.uuid_slug
    prod_id_list = [p.meta["id"] for p in prod_list]
    product_list = [ProductFactory.create(es_id=es_id) for es_id in prod_id_list]
    willorders_ws_db_session.commit()

    obj_list = OrderFactory.create_batch(2, user_slug=user_slug)

    for product in product_list:
        OrderProductFactory.create(order=obj_list[0], product=product, amount=2)

    for product in product_list[0:3]:
        OrderProductFactory.create(order=obj_list[1], product=product, amount=5)

    willorders_ws_db_session.commit()

    response = auth_session.post(
        domain_url + "/api/order/user"
    )

    data = response.json()
    UserOrdersSchema().load(data)
    assert response.status_code == 200
    assert len(data["orders"]) == 2
    assert data["total"] == 2
    assert data["pages"] == 1

    order_slug_list = [order["slug"] for order in data["orders"]]
    for slug in order_slug_list:
        assert slug in [obj.uuid_slug for obj in obj_list]

    for order in data["orders"]:
        if order["slug"] == obj_list[0].uuid_slug:
            assert order["product_types"] == 5
            assert order["items_amount"] == 10
        else:
            assert order["product_types"] == 3
            assert order["items_amount"] == 15

    response = auth_session.post(
        domain_url + "/api/order/user",
        json={
            "page": "1",
            "page_size": "1"
        }
    )

    data = response.json()
    UserOrdersSchema().load(data)
    assert response.status_code == 200
    assert len(data["orders"]) == 1
    assert data["total"] == 2
    assert data["pages"] == 2

    response = auth_session.post(
        domain_url + "/api/order/user",
        json={
            "datespan": {
                "start": str(date.today() - timedelta(days=1)),
                "end": str(date.today() + timedelta(days=1))
            }
        }
    )

    data = response.json()
    UserOrdersSchema().load(data)
    assert response.status_code == 200
    assert len(data["orders"]) == 2
    assert data["total"] == 2
    assert data["pages"] == 1


def test_select_from_user_no_order(domain_url, auth_user, auth_session):
    response = auth_session.post(
        domain_url + "/api/order/user"
    )

    with pytest.raises(JSONDecodeError):
        response.json()

    assert response.status_code == 204


def test_select_from_user_unauthorized(domain_url):
    response = requests.post(
        domain_url + "/api/order/user",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
