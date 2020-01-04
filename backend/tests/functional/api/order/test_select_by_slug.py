import pytest
import requests
from uuid import uuid4

from webservices.willorders.backend.tests.factories import OrderFactory, ProductFactory, OrderProductFactory
from backend.util.response.order.order import OrderSchema
from backend.util.response.error import ErrorSchema
from backend.util.slug import uuid_to_slug


@pytest.fixture(scope="function", autouse=True)
def factory_session(willorders_ws_db_session):
    OrderFactory._meta.sqlalchemy_session = willorders_ws_db_session
    ProductFactory._meta.sqlalchemy_session = willorders_ws_db_session
    OrderProductFactory._meta.sqlalchemy_session = willorders_ws_db_session


def test_select_by_slug(domain_url, auth_user, auth_session, es_create, willorders_ws_db_session):
    prod_list = es_create("products", 5)
    user_slug = auth_user.uuid_slug
    obj = OrderFactory.create(user_slug=user_slug)
    willorders_ws_db_session.commit()

    slug = obj.uuid_slug
    prod_id_list = [p.meta["id"] for p in prod_list]

    amount = 1
    for es_id in prod_id_list:
        product = ProductFactory.create(es_id=es_id)
        OrderProductFactory.create(order=obj, product=product, amount=amount)
        amount += 1

    willorders_ws_db_session.commit()

    response = auth_session.get(
        domain_url + "/api/order/%s" % slug
    )

    data = response.json()
    OrderSchema().load(data)
    assert response.status_code == 200
    assert data["slug"] == slug
    assert data["product_types"] == len(prod_list)
    assert data["items_amount"] == ((1 + len(prod_list)) * len(prod_list)) / 2
    assert len(data["products"]) == len(prod_list)

    for item in [item.to_dict() for item in obj.items]:
        product = next(p for p in data["products"] if p["id"] == item["item_id"])
        assert product["amount"] == item["amount"]

    response = auth_session.get(
        domain_url + "/api/order/WILLrogerPEREIRAslugBR"
    )

    data = response.json()
    assert data["error"] == {}
    assert response.status_code == 404


def test_select_by_slug_wrong_user(domain_url, auth_session, es_create, willorders_ws_db_session):
    prod_list = es_create("products", 3)
    user_slug = uuid_to_slug(uuid4())
    obj = OrderFactory.create(user_slug=user_slug)
    willorders_ws_db_session.commit()

    slug = obj.uuid_slug
    prod_id_list = [p.meta["id"] for p in prod_list]

    amount = 1
    for es_id in prod_id_list:
        product = ProductFactory.create(es_id=es_id)
        OrderProductFactory.create(order=obj, product=product, amount=amount)
        amount += 1

    willorders_ws_db_session.commit()

    response = auth_session.get(
        domain_url + "/api/order/%s" % slug
    )

    data = response.json()
    assert data["error"] == {}
    assert response.status_code == 404


def test_select_by_slug_unauthorized(domain_url):
    response = requests.get(
        domain_url + "/api/order/WILLrogerPEREIRAslugBR",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
