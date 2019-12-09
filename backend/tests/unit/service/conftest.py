import pytest


@pytest.fixture(scope="function")
def service_init_mock(mocker):
    MockDBSession = mocker.patch("backend.dao.postgres_db.DBSession")

    def mock_init(self):
        self.db_session = MockDBSession()

    return mock_init
