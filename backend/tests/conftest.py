import pytest
import re
import os
import json
import gzip
from dotenv import load_dotenv, find_dotenv
from elasticsearch_dsl import Index
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vcr import VCR

from .factories import OAuthFactory, UserFactory
from backend import create_app
from backend.controller.auth import bplogin
from backend.model import OAuth, User
from webservices.willstores.backend.dao.es import ES
from webservices.willstores.backend.tests.factories import ProductFactory, SessionFactory
from webservices.willorders.backend.model import Order, Product


test_factory = sessionmaker()


@pytest.fixture(scope="session")
def domain_ip():
    load_dotenv(find_dotenv())
    return os.getenv("TEST_DOMAIN_IP")


@pytest.fixture(scope="session")
def database_url(domain_ip):
    test_db = os.getenv("TEST_DATABASE_URL")
    TEST_DATABASE_URL = re.sub("TEST_DOMAIN_IP", domain_ip, test_db)
    return TEST_DATABASE_URL


class FlaskLoginClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        fresh = kwargs.pop("fresh_login", True)

        super(FlaskLoginClient, self).__init__(*args, **kwargs)

        if user:
            with self.session_transaction() as sess:
                sess["user_id"] = user.get_id()
                sess["_fresh"] = fresh


@pytest.fixture(scope="session")
def flask_app(domain_ip):
    app = create_app(flask_env="test")
    app.config["WILLSTORES_WS"] = "http://" + domain_ip + ":8001"
    app.config["WILLORDERS_WS"] = "http://" + domain_ip + ":8002"
    app.test_client_class = FlaskLoginClient
    return app


@pytest.fixture(scope="session")
def db_connection(database_url):
    engine = create_engine(database_url)
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db_session(db_connection):
    transaction = db_connection.begin()
    session = test_factory(bind=db_connection)
    yield session
    session.close()
    transaction.rollback()


@pytest.fixture(scope="session")
def db_perm_connection(database_url):
    engine = create_engine(database_url)
    test_factory.configure(bind=engine)
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db_perm_session(db_perm_connection):
    session = test_factory(bind=db_perm_connection)
    yield session
    session.query(OAuth).delete()
    session.query(User).delete()
    session.commit()
    session.close()


@pytest.fixture(scope="session", autouse=True)
def setup_teardown(database_url, db_perm_connection):
    os.environ["DATABASE_URL"] = database_url
    session = test_factory(bind=db_perm_connection)
    session.query(User).delete()
    session.query(OAuth).delete()
    session.commit()
    session.close()
    create_app(flask_env="test").test_client().post("test")
    yield
    session = test_factory(bind=db_perm_connection)
    session.query(User).delete()
    session.query(OAuth).delete()
    session.commit()
    session.close()


@pytest.fixture(scope="session")
def test_vcr():
    import logging
    logging.basicConfig()
    vcr_log = logging.getLogger("vcr")
    vcr_log.setLevel(logging.INFO)

    return VCR(
        serializer="yaml",
        cassette_library_dir=os.path.join(os.path.dirname(__file__), "cassettes"),
        record_mode="once",
        ignore_localhost=True,
        ignore_hosts=["willbuyer.com"],
        match_on=["method", "scheme", "host", "port", "path", "query"],
        filter_headers=[("authorization", "===HIDDEN===")]
    )


@pytest.fixture(scope="function")
def auth_user(db_perm_session, test_vcr):
    UserFactory._meta.sqlalchemy_session = db_perm_session
    OAuthFactory._meta.sqlalchemy_session = db_perm_session
    user = UserFactory.create(provider="google")
    oauth = OAuthFactory.create(provider="google")
    oauth.user = user

    with test_vcr.use_cassette("auth_blueprint.yml") as cass:
        if len(cass.responses) > 0:
            provider_user_id = json.loads(gzip.decompress(cass.responses[0]["body"]["string"]))["id"]
            user.provider_user_id = provider_user_id
            oauth.provider_user_id = provider_user_id

    db_perm_session.commit()
    return user


@pytest.fixture(scope="function")
def auth_blueprint(monkeypatch, db_perm_session, test_vcr):
    monkeypatch.setattr(bplogin.storage, "session", db_perm_session)
    token = {"access_token": "fake_token"}
    bplogin.session.token = token
    with test_vcr.use_cassette("auth_blueprint.yml"):
        yield bplogin


# WILLSTORES_WS related fixtures##########################################
@pytest.fixture(scope="session")
def es_object(domain_ip):
    os.environ["ES_URL"] = "http://%s:9200" % domain_ip
    es = ES()
    yield es


@pytest.fixture(scope="session")
def es_create(es_object):
    def execute(doc_type, amount, **kwargs):
        if doc_type == "sessions":
            obj_list = SessionFactory.create_batch(amount, **kwargs)
        else:
            obj_list = ProductFactory.create_batch(amount, **kwargs)

        [obj.save(using=es_object.connection) for obj in obj_list]
        Index("store", using=es_object.connection).refresh()
        return obj_list

    yield execute
    Index("store", using=es_object.connection).delete()


# WILLORDERS_WS related fixtures##########################################
willorders_ws_test_factory = sessionmaker()


@pytest.fixture(scope="session")
def willorders_ws_db_connection(domain_ip):
    test_db = os.getenv("WILLORDERS_WS_DATABASE_URL")
    database_url = re.sub("TEST_DOMAIN_IP", domain_ip, test_db)
    engine = create_engine(database_url)
    willorders_ws_test_factory.configure(bind=engine)
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def willorders_ws_db_session(willorders_ws_db_connection):
    session = willorders_ws_test_factory(bind=willorders_ws_db_connection)
    yield session
    session.query(Order).delete()
    session.query(Product).delete()
    session.commit()
    session.close()
