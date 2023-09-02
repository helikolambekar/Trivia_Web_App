from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


from . import db, mail
from .models import Player, Game, Question

auth = Blueprint("auth", __name__)


# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #make the email in lower case
        email = email.lower()
        
        # Check the email exist in the database
        user = Player.query.filter_by(email=email).first()

        if user:
            # Check the password equal to the user's password in database
            if check_password_hash(user.password, password):
                flash('Logged in successful', category='success')

                # User login and remember the user
                login_user(user, remember=True)

                # check if super user
                if user.admin == 1:
                    return redirect(url_for('views.display_admin', user=current_user))
                else:
                    # TODO: need to redirect to the home page
                    return redirect(url_for('views.main', user=current_user))

            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('email does not exist.', category='error')
    return render_template("login.html", user=current_user)


# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', category='success')
    return redirect(url_for('views.main'))


# Sign up route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        player_name = request.form.get('playerName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        #make the email in lower case
        email = email.lower()
        
        user = Player.query.filter_by(email=email).first()
        # Check the email already exists or not
        if user:
            flash('Email already exists.', category='error')
        # Check length of the email
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        # Check the username
        elif len(player_name) < 2:
            flash('Player name must be greater than 1 characters.', category='error')
        # Check the length of password and
        # TODO: add regular expression later
        elif len(password1) < 7:
            flash('password must be at least 7 characters.', category='error')
        # Check the password and comfirmed password
        elif password1 != password2:
            flash('password don\'t match', category='error')
        else:
            # create add new user to the test database
            new_player = Player(email=email, player_name=player_name,
                                password=generate_password_hash(password1, method='sha256'), admin=False)
            db.session.add(new_player)
            db.session.commit()

            # create a game for the player
            total_num_questions = Question.query.count()
            game = Game(type='TEST', lives=3, score=0, question_time=30,
                        num_skip_question=3, questions_left=str(0),
                        answer_location=0, max_questions=total_num_questions,
                        num_fifty_fifty=3, fifty_fifty_option=str(0),
                        player_id=new_player)
            db.session.add(game)
            db.session.commit()

            # immediately login after created account
            login_user(new_player, remember=True)

            flash('Account created!', category='success')
            return redirect(url_for('views.main', user=current_user))

            # login the user after created account, and remember it
            # TODO: after we sign up, where should we direct to?

    return render_template('sign_up.html', user=current_user)


# sending email that includes the link of resetting password
def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@source.com')
    msg.body = f''' To reset your password. Please follow the link below:

    {url_for('auth.reset_token', token=token, _external=True)}

    This link is only valid for 5 minutes.
    If you didn't send a password reset request. Please ignore this message.
    
    
    '''
    mail.send(msg)


# route for entering email to get the link of resetting password
@auth.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        
        #make the email in lower case
        email = email.lower()
        
        user = Player.query.filter_by(email=email).first()
        if user:
            send_mail(user)
            flash('Reset Request sent. Check your email.', 'success')
            return redirect(url_for('auth.login', user=current_user))
        elif user is None:
            flash('Please Enter a email')
    return render_template('reset_request.html', user=current_user)


# route for resetting password
@auth.route('/reset_request/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Player.verify_token(token)
    if user is None:
        flash('That is invalid token or expired. Please try again.', 'warning')
        return redirect(url_for('auth.reset_request', user=current_user))

    if request.method == 'POST':
        new_password_1 = request.form['password']
        new_password_2 = request.form['confirm_password']

        # Check the length of password
        if len(new_password_1) < 7:
            flash('password must be at least 7 characters.', category='error')
            return redirect(url_for('auth.reset_token', token=token, user=current_user))
        # Check the password and comfirmed password
        elif new_password_1 != new_password_2:
            flash('password don\'t match', category='error')
            return redirect(url_for('auth.reset_token', token=token, user=current_user))

        user.password = generate_password_hash(new_password_1, method='sha256')
        db.session.commit()
        flash('Password changed! Please login!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('change_password.html', user=current_user)
