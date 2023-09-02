from main import create_app


def test_change_to_duplicate_email():
    flask_app = create_app("DEV")

    with flask_app.test_client() as client:
        email1 = 'email1@mail.com'
        email2 = 'email2@mail.com'
        password1 = 'password1'
        password2 = 'password2'
        username1 = 'user1'
        username2 = 'user2'

        # First sign-up two users
        signup(client, email1, username1, password1)
        logout(client)
        signup(client, email2, username2, password2)
        logout(client)

        login(client, email2, password2)
        
        rv = edit_email(client, email1)
        assert b'Email already exists.' in rv.data



def test_change_email():
    flask_app = create_app("DEV")

    with flask_app.test_client() as client:
        email = 'email@mail.com'
        password = 'password'
        username = 'user'
        new_email = 'newemail@mail.com'

        # sign up a new user
        signup(client, email, username, password)
        logout(client)

        login(client, email, password)

        rv = edit_email(client, new_email)
        assert new_email.encode('utf_8') in rv.data
        rv = edit_email(client, email)
        assert email.encode('utf_8') in rv.data


def test_change_username():
    flask_app = create_app("DEV")

    with flask_app.test_client() as client:
        email = 'email@mail.com'
        password = 'password'
        username = 'user'
        new_username = 'newuser'

        # sign up a new user
        signup(client, email, username, password)
        logout(client)

        login(client, email, password)

        rv = edit_username(client, new_username)
        assert new_username.encode('utf_8') in rv.data

def test_change_password():
    flask_app = create_app("DEV")

    with flask_app.test_client() as client:
        email = 'email@mail.com'
        password = 'password'
        username = 'user'
        new_password = 'newuser1'

        # sign up a new user
        signup(client, email, username, password)
        logout(client)

        login(client, email, password)

        # change the password and try to log in
        edit_password(client, new_password)
        rv = login(client, email, new_password)
        assert b"Logged in successful" in rv.data

        # change the password back, as other tests use this password
        edit_password(client, password)


def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def signup(client, email, name, password):
    return client.post('/sign-up', data=dict(
        email=email,
        playerName=name,
        password1=password,
        password2=password
    ), follow_redirects=True)


def edit_email(client, email):
    return client.post('/player_profile/edit_email', data=dict(
        email=email
    ), follow_redirects=True)


def edit_username(client, username):
    return client.post('/player_profile/edit_username', data=dict(
        username=username
    ), follow_redirects=True)

def edit_password(client, password):
    return client.post('/player_profile/edit_password', data=dict(
        password1 = password,
        password2 = password
    ), follow_redirects=True)