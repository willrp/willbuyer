import pytest

from backend.dao.postgres_db import init_db


def test_postgres_db():
    init_db()


def test_postgres_db_error(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("DATABASE_URL", "postgresql://will:roger@churros:5432/pereira")
        with pytest.raises(SystemExit):
            init_db()

    init_db()
