import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "WILLSECRET"
    ERROR_404_HELP = False
    ERROR_INCLUDE_MESSAGE = False
    TEST_DOMAIN_IP = os.getenv("TEST_DOMAIN_IP")
    WILLSTORES_WS = os.getenv("WILLSTORES_WS")
    WILLORDERS_WS = os.getenv("WILLORDERS_WS")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY", default=BaseConfig.SECRET_KEY)


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
