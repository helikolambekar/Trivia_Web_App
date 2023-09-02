from flask import Blueprint, redirect, url_for, request, flash

from . import db
from .models import Player
from flask_login import current_user

player_profile = Blueprint('player_profile', __name__)


@player_profile.route('/player_profile/edit_username', methods=['GET', 'POST'])
def edit_username():
    if request.method == 'POST':
        new_username = request.form['username']
        cur_username = current_user.player_name

        # Check the username
        if len(new_username) < 2:
            flash('Player name must be greater than 1 characters.', category='error')
            return redirect(url_for('views.userProfile'))

        # TODO: Check if new user name is different from current. Can skip some steps if they are not.

        cur_userid = current_user.id

        user = Player.query.filter_by(id=cur_userid).first()
        user.player_name = new_username
        db.session.commit()

        return redirect(url_for('views.userProfile'))


@player_profile.route('/player_profile/edit_email', methods=['GET', 'POST'])
def edit_email():
    if request.method == 'POST':
        new_email = request.form['email']
        cur_email = current_user.email

        existing_user = Player.query.filter_by(email=new_email).first()
        # Check the email already exists or not
        if existing_user:
            flash('Email already exists.', category='error')
            return redirect(url_for('views.userProfile'))
        # Check length of the email
        elif len(new_email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
            return redirect(url_for('views.userProfile'))

        # TODO: Check if new user email is different from current. Can skip some steps if they are not.

        cur_userid = current_user.id

        user = Player.query.filter_by(id=cur_userid).first()
        user.email = new_email
        db.session.commit()

        return redirect(url_for('views.userProfile'))


@player_profile.route('/player_profile/edit_password', methods=['GET', 'POST'])
def edit_password():
    from werkzeug.security import generate_password_hash
    if request.method == 'POST':
        new_password_1 = request.form['password1']
        new_password_2 = request.form['password2']

        # Check the length of password and
        if len(new_password_1) < 7:
            flash('password must be at least 7 characters.', category='error')
            return redirect(url_for('views.userProfile'))
        # Check the password and comfirmed password
        elif new_password_1 != new_password_2:
            flash('password don\'t match', category='error')
            return redirect(url_for('views.userProfile'))

        cur_userid = current_user.id

        user = Player.query.filter_by(id=cur_userid).first()
        user.password = generate_password_hash(new_password_1, method='sha256')
        db.session.commit()

        return redirect(url_for('views.userProfile'))
