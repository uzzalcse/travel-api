import pytest
from app import app as flask_app

@pytest.fixture
def app():
    """
    Flask app fixture for testing.
    """
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """
    Test client fixture for Flask app.
    """
    return app.test_client()
