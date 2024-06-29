from main import create_app, create_api
from app.urls import add_urls
import pytest
from app import database
from app.models import Racer, Car, Duration

MODELS = [Racer, Car, Duration]


@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture()
def client(app):
    api = create_api(app)
    add_urls(api)
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_database_path(mocker):
    mocker.patch.object(database, 'database_path', ':memory:')
    test_db = database.connect_db()
    test_db.create_tables(MODELS)
    return test_db
