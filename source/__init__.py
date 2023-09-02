from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_mail import Mail

from .helper_functions.dev_import_questions import populate_db
from .helper_functions.dev_import_admin import populate_admin_to_db
from .helper_functions.prod_test_db import db_exists

db = SQLAlchemy()
DB_NAME = "test.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgsar3wdgrgdsfsdg90kl4512km12asdhtw'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'knowitall.game@gmail.com'
app.config['MAIL_PASSWORD'] = 'CS673team1'
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


def create_app(ENV):
    
    if ENV == "PROD":
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("://", "ql://", 1)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
   
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .question import question
    from .leaderboard import leaderboard
    from .game import game
    from .auth import auth
    from .category import category
    from .player_profile import player_profile
    from .admin import admin
    from .models import Player
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(question, url_prefix='/')
    app.register_blueprint(leaderboard, url_prefix='/')
    app.register_blueprint(game, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(category, url_prefix='/')
    app.register_blueprint(player_profile, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    if ENV == 'DEV':
        create_database(app)
    else:
        create_database_prod(app)
        
    # login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # define a function for loading the player
    @login_manager.user_loader
    def load_user(id):
        return Player.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("source/" + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        os.chdir("source")
        populate_db()

        # create super user account
        populate_admin_to_db(1, 'admin@test.com', '12345678', 'Admin', 1, True)
        # it will cause issues if does to change the working directory back
        os.chdir("../")
    else:
        print("Database found")

def create_database_prod(app):
    if db_exists() == False:
        print("No Tables in DB")
        
        db.create_all(app=app)
        print("Creating Tables")
    else:
        print("tables exist")