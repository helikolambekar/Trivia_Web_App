from main import create_app
from source.models import Game
from source import db
import pytest


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app("DEV")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"KNOWITALL" in response.data
    assert b"START" in response.data
    assert b"LeaderBoard" in response.data
    assert b"About" in response.data


def test_category_page(test_client):
    response = test_client.get('/category')
    assert response.status_code == 200
    assert b"START" in response.data
    assert b"GEOGRAPHY" in response.data
    assert b"ART" in response.data
    assert b"COMPUTER SCIENCE" in response.data
    assert b"SCIENCE" in response.data
    assert b"MYTHOLOGY" in response.data
    assert b"TV SHOWS" in response.data
    assert b"MOVIE" in response.data
    assert b"ALL" in response.data


def test_game_page(test_client):
    response = test_client.get('/game')
    assert response.status_code == 200
    assert b"LIVES" in response.data
    assert b"SCORE" in response.data
    assert b"TIME" in response.data
    assert b"Lifelines" in response.data
    assert b"Next Question" in response.data
    assert b"Submit" in response.data
    assert b"QUIT GAME" in response.data
    assert b"Skip Question" in response.data
    assert b"50/50" in response.data


def test_leaderboard_page(test_client):
    login(test_client, 'admin@test.com', '12345678')
    response = test_client.get('/leaderboard')
    assert response.status_code == 200  
    assert b"Category" in response.data
    assert b"Username" in response.data
    assert b"Score" in response.data

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)