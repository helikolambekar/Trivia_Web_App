from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from flask_login import current_user, login_required
from . import db
from .models import Player, LeaderboardScore, Question
import json

admin = Blueprint('admin', __name__)

# route to the test-feature page
@admin.route('/admin/players', methods=['GET', 'POST'])
@login_required
def show_players():
    #user = Player.query.filter_by(id=current_user.id).first()

    # checking if it is superuser
    #if user.admin == 1:
    if is_super_user(current_user):
        players = Player.query.all()
        return render_template('admin/delete_player.html', user=current_user, players=players)
    else:
        flash('You are not allow to go to admin page.', category='error')
    return render_template('main.html', user=current_user)

# route for the delete-user function
@admin.route('/admin/delete-player', methods=['POST'])
def delete_player():
    print("DELETING PLAYER")
    player = json.loads(request.data)
    playerId = player['playerId']
    player = Player.query.get(playerId)
    if player:
        db.session.delete(player)
        db.session.commit()

    return jsonify({})

# route the admin question page
@admin.route('admin/question')
@login_required
def questions():
    if is_super_user(current_user):
        question = Question.query.order_by(Question.category.desc()).all()
        return render_template('admin/questions.html', user=current_user, question=question)
    else:
        flash('You are not allow to go to admin page.', category='error')
    return render_template('main.html', user=current_user)


# route add new question
@admin.route('admin/question/new')
@login_required
def new():
    if is_super_user(current_user):
        return render_template('admin/new_question.html', user=current_user)
    else:
        flash('You are not allow to go to admin page.', category='error')
    return render_template('main.html', user=current_user)


# route edit question
@admin.route('admin/question/edit', methods=['POST'])
@login_required
def edit():
    if is_super_user(current_user):
        id = request.form.get('question_id')
        question = Question.query.filter_by(id=id).first()
       
        return render_template('admin/edit_question.html', user=current_user, question=question)   
    else:
        flash('You are not allow to go to admin page.', category='error')
        return render_template('main.html', user=current_user)


# add new question to db
@admin.route('admin/question/add_question', methods=['POST', 'GET'])
@login_required
def add_question():
    if request.method == 'POST':
        category = request.form.get('category')
        question = request.form.get('question')
        answer = request.form.get('answer')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')

        # compare if the question is already exist.
        q = Question.query.filter_by(question=question).first()
        
        if q:
            flash('Question already exists.', category='error')

            # add new question to db
        else:
            new_question = Question(category=category, question=question,
                                    answer=answer, option_1=option1,
                                    option_2=option2, option_3=option3)
            db.session.add(new_question) 
            db.session.commit()
            flash('Question added!', category='success')
            return redirect(url_for('admin.questions', user=current_user))
    return render_template("admin/new_question.html", user=current_user)


# edit selected question
@admin.route('admin/question/edit_question', methods=['POST'])
@login_required
def edit_question():
    print(request.form)
    q_id = request.form.get('question_id')
    q = Question.query.filter_by(id=q_id).first()
    q.category = request.form.get('category')
    q.question = request.form.get('question')
    q.answer   = request.form.get('answer')
    q.option_1 = request.form.get('option_1')
    q.option_2 = request.form.get('option_2')
    q.option_3 = request.form.get('option_3')
           
    db.session.commit()
    flash('Question Editted Suceefully!', category='success')
    return render_template("admin/edit_question.html", question=q, user=current_user)


# delete selected question
@admin.route('admin/delete_question', methods=['POST'])
@login_required
def delete_question():
    id = request.form.get('question_id')
    q = Question.query.filter_by(id=id).first()
    db.session.delete(q)
    db.session.commit()
    flash('Delete success!', category='success')
    return redirect(url_for('admin.questions'))


# delete selected score
@admin.route('admin/delete_score', methods=['POST'])
@login_required
def delete_score():
    id = request.form.get('score_id')
    score = LeaderboardScore.query.filter_by(id=id).first()
    db.session.delete(score)
    db.session.commit()
    flash('Delete success!', category='success')
    return redirect(url_for('views.leaderBoard'))

#---------HELP FUNCTIONS---------------------
def is_super_user(current_user):
    user = Player.query.filter_by(id=current_user.id).first()
    if user.admin == 1:
        return True
    else:
        return False