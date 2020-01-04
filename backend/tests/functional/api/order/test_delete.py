import pytest
import requests
from uuid import uuid4

from backend.util.response.error import ErrorSchema
from backend.util.slug import uuid_to_slug
from webservices.willorders.backend.tests.factories import OrderFactory, ProductFactory, OrderProductFactory
from webservices.willorders.backend.model import Order, Product, OrderProduct


@pytest.fixture(scope="function", autouse=True)
def factory_session(willorders_ws_db_session):
    OrderFactory._meta.sqlalchemy_session = willorders_ws_db_session
    ProductFactory._meta.sqlalchemy_session = willorders_ws_db_session
    OrderProductFactory._meta.sqlalchemy_session = willorders_ws_db_session


def test_delete(domain_url, auth_user, auth_session, es_create, willorders_ws_db_session):
    prod_list = es_create("products", 5)
    user_slug = auth_user.uuid_slug
    obj = OrderFactory.create(user_slug=user_slug)
    willorders_ws_db_session.commit()

    slug = obj.uuid_slug
    prod_id_list = [p.meta["id"] for p in prod_list]

    for es_id in prod_id_list:
        product = ProductFactory.create(es_id=es_id)
        OrderProductFactory.create(order=obj, product=product, amount=2)

    willorders_ws_db_session.commit()

    assert len(willorders_ws_db_session.query(Order).all()) == 1
    assert len(willorders_ws_db_session.query(Product).all()) == 5
    assert len(willorders_ws_db_session.query(OrderProduct).all()) == 5

    response = auth_session.delete(
        domain_url + "/api/order/delete/%s" % slug
    )

    data = response.json()
    assert data == {}
    assert response.status_code == 200
    assert len(willorders_ws_db_session.query(Order).all()) == 0
    assert len(willorders_ws_db_session.query(Product).all()) == 5
    assert len(willorders_ws_db_session.query(OrderProduct).all()) == 0

    response = auth_session.delete(
        domain_url + "/api/order/delete/%s" % slug
    )

    data = response.json()
    assert data["error"] == {}
    assert response.status_code == 404
    assert len(willorders_ws_db_session.query(Order).all()) == 0
    assert len(willorders_ws_db_session.query(Product).all()) == 5
    assert len(willorders_ws_db_session.query(OrderProduct).all()) == 0


def test_delete_wrong_user(domain_url, auth_session, es_create, willorders_ws_db_session):
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

    response = auth_session.delete(
        domain_url + "/api/order/delete/%s" % slug
    )

    data = response.json()
    assert data["error"] == {}
    assert response.status_code == 404


def test_delete_unauthorized(domain_url):
    response = requests.delete(
        domain_url + "/api/order/delete/WILLrogerPEREIRAslugBR",
        verify=False
    )

    data = response.json()
    ErrorSchema().load(data)
    assert response.status_code == 401
