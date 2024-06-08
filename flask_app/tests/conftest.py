import pytest
from app import create_app
from app.utils.sql.db import db

@pytest.fixture()
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
