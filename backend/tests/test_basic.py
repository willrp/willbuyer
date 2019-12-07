import pytest

from backend import create_app


def test_create_app_default():
    create_app("test")


def test_create_app_no_env_variable():
    with pytest.raises(SystemExit):
        create_app()


def test_create_app_wrong_key():
    with pytest.raises(SystemExit):
        create_app("dontexist")


def test_create_app_from_env_var(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("FLASK_ENV", "test")
        create_app()


def test_create_app_env_var_and_flask_config_same(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("FLASK_ENV", "test")
        create_app("test")


def test_create_app_env_var_and_flask_config_different(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("FLASK_ENV", "test")
        with pytest.raises(SystemExit):
            create_app("development")


def test_create_app_env_var_and_flask_config_wrong(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("FLASK_ENV", "will")
        with pytest.raises(SystemExit):
            create_app("will")
