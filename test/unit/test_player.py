from main import create_app

def test_player():
    flask_app = create_app("DEV")

    with flask_app.test_client("DEV") as client:

        playerEmail1 = "test1@gmail.com"
        playerName1 = "playerName1"
        password1 = "password1"

        rv = signUp(client, playerEmail1, playerName1, password1, password1)
        rv = login(client, playerEmail1, password1)
        assert b'Logged' in rv.data

        rv = logout(client)
        assert b'Logout' in rv.data


def login(client, playerEmail, password):
    return client.post('/login', data=dict(
        email=playerEmail,
        password=password
        ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def signUp(client, playerEmail, playerName, password1, password2):
    return client.post('/sign-up', data=dict(
        email=playerEmail,
        playerName=playerName,
        password1=password1,
        password2=password2
    ), follow_redirects=True)
