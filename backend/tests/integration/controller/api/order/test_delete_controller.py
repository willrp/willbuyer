import pytest
from flask import json

from backend.util.response.error import ErrorSchema
from webservices.willorders.backend.tests.factories import OrderFactory, ProductFactory, OrderProductFactory
from webservices.willorders.backend.model import Order, Product, OrderProduct


@pytest.fixture(scope="function", autouse=True)
def factory_session(willorders_ws_db_session):
    OrderFactory._meta.sqlalchemy_session = willorders_ws_db_session
    ProductFactory._meta.sqlalchemy_session = willorders_ws_db_session
    OrderProductFactory._meta.sqlalchemy_session = willorders_ws_db_session


def test_delete_controller(flask_app, auth_user, es_create, willorders_ws_db_session):
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

    with flask_app.test_client(user=auth_user) as client:
        response = client.delete(
            "api/order/delete/%s" % slug
        )

    data = json.loads(response.data)
    assert data == {}
    assert response.status_code == 200
    assert len(willorders_ws_db_session.query(Order).all()) == 0
    assert len(willorders_ws_db_session.query(Product).all()) == 5
    assert len(willorders_ws_db_session.query(OrderProduct).all()) == 0

    with flask_app.test_client(user=auth_user) as client:
        response = client.delete(
            "api/order/delete/%s" % slug
        )

    data = json.loads(response.data)
    assert data["error"] == {}
    assert response.status_code == 404
    assert len(willorders_ws_db_session.query(Order).all()) == 0
    assert len(willorders_ws_db_session.query(Product).all()) == 5
    assert len(willorders_ws_db_session.query(OrderProduct).all()) == 0


def test_delete_controller_unauthorized(flask_app):
    with flask_app.test_client() as client:
        response = client.delete(
            "api/order/delete/WILLrogerPEREIRAslugBR",
        )

    data = json.loads(response.data)
    ErrorSchema().load(data)
    assert response.status_code == 401
