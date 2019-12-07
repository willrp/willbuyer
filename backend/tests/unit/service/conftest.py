import pytest


@pytest.fixture(scope="function")
def service_init_mock(mocker):
    with mocker.patch("backend.dao.postgres_db.DBSession") as MockDBSession:
        def mock_init(self):
            self.db_session = MockDBSession()

        return mock_init
