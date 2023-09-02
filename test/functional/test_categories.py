from main import create_app
from source.models import Game, Player
from flask_login import current_user
import json

#This test is to determine that the Category Select page is working properly for a logged in which includes 1) initializing the game variables and 2) setting the selected category
def test_category_select_logged_in():
    flask_app = create_app("DEV")

    with flask_app.test_client() as test_client:
        #This should be a test login account
        login(test_client, 'admin@test.com', '12345678')
        data = {
            'category': 'Science',
        }

        response = test_client.post(
                "/category/select",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )

        p = Player.query.get(current_user.id)
        new_game = Game.query.get(p.game_id)
        #Make sure cateogry post request was successful
        assert response.status_code == 200
        
        #Check that category was properly set and game was otherwise initialized
        assert new_game.category == "Science"
        assert new_game.lives == 3

#This test ensures that selecting a category also works when not logged in
def test_category_select_not_logged_in():
    flask_app = create_app("DEV")

    with flask_app.test_client() as test_client:
        data = {
            'category': '',
        }

        response = test_client.post(
                "/category/select",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )

        #Make sure cateogry post request was successful
        assert response.status_code == 200
        


def login(client, playerEmail, password):
    return client.post('/login', data=dict(
        email=playerEmail,
        password=password
        ), follow_redirects=True)