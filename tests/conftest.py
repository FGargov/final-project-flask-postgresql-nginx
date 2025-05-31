import pytest
import os
import sys

from app.app import app as flask_app
from app.models import db


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()
            yield client
            db.drop_all()
