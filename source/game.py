from flask import Blueprint, jsonify, request
from flask_login import current_user
from datetime import datetime
import random, math
from main import ENV

from sqlalchemy.sql.expression import null
from . import db
from .models import Game, Question, Player

game = Blueprint('game', __name__)


@game.route('/game/settings', methods=['GET', 'POST'])
def gameSettings():
    # get the gameID from the user's browser's local memory
    gameID = get_gameID()
    game = get_game(gameID)

    # Check if the category is defined, and if so set the game.category data to the category. Parse the questions table to get every id from that category
    # Set up the conditional logic for the initialization of the questions_left array to only populate with valued from the category.

    # get all QuestionIDs and randomize them
  
    total_question_tuples = Question.query.with_entities(Question.id).all()
    
    total_questions = []
    for question in total_question_tuples:
        total_questions.append(int(question[0]))
           
    questions_left = random.sample(total_questions, len(total_questions))
    print("ALL IDS: " + str(questions_left))
    
    # filter out questions that are not in the game's category
    if game.category != "All":
        fitered_questions_left = []
        print("CATEGORY:" + str(game.category))
        for k in questions_left:
                  
            q = Question.query.get(k)
        
            if q.category == game.category:
                fitered_questions_left.append(q.id)
        questions_left = random.sample(fitered_questions_left, len(fitered_questions_left))

    print("FILTRED QUESTION IDs:")
    print(questions_left)
    # select the random question for the first question
    str_id = questions_left[0]
    q = Question.query.get(str_id)

    # Shuffle the 4 potential answers
    input = [q.answer, q.option_1, q.option_2, q.option_3]
    answers = random.sample(input, len(input))

    # Determine the location of the answer
    for x in range(4):
        if answers[x] == q.answer:
            answer_location = x + 1

    # Remove the question from the questions left array
    questions_left.remove(str_id)

    # pass all the question information to the game object
    game.questions_left = str(questions_left)
    game.question = str_id
    game.answer_location = answer_location
    game.cr_time = datetime.now()
    db.session.commit()

    # Define the data to be handed off to the template
    return_data = [{"Lives": game.lives}, {"Question Time": game.question_time}, {"Score": game.score},
                   {"Number Question Skips": game.num_skip_question},
                   {"Question": q.question}, {"Option_1": answers[0]}, {"Option_2": answers[1]},
                   {"Option_3": answers[2]}, {"Option_4": answers[3]}, {"Fifth Fifty Attempt": game.num_fifty_fifty},
                   {"game_id": game.id}]

    # data to be returned to user
    print(return_data)
    return jsonify(return_data)


# Return the answer to the current question
@game.route('/game/answer')
def gameAnswer():
    # get the gameID from the user's browser's local memory
    gameID = get_gameID()
    game = get_game(gameID)

    return_data = [{"Answer_Location": game.answer_location}]
    return (jsonify(return_data))


# Modify the game's lives
@game.route('/game/removelife')
def removeLife():
    # get the gameID from the user's browser's local memory
    gameID = get_gameID()
    game = get_game(gameID)

    game.lives = game.lives - 1
    db.session.commit()
    return (str(game.lives))


# Modify the game's remaining question skips
@game.route('/game/skip_question')
def skipQuestion():
    # get the gameID from the user's browser's local memory
    gameID = get_gameID()
    game = get_game(gameID)
    game.num_skip_question = game.num_skip_question - 1
    db.session.commit()

    return (str(game.num_skip_question))


# Modify the game's remaining 50/50, and get the options that can be removed
@game.route('game/fifty_fifty')
def fiftyFifty():
    # get the gameID from the user's browser's local memory
    gameID = get_gameID()
    game = get_game(gameID)
    option = []
    game.num_fifty_fifty = game.num_fifty_fifty - 1
    attempt = str(game.num_fifty_fifty)

    for i in range(1, 4):
        if i != game.answer_location:
            option.append(i)
    game.fifty_fifty_option = str(option)
    return_data = [{"first_option": game.fifty_fifty_option[1]},
                   {"second_option": game.fifty_fifty_option[4]},
                   {"attempt": attempt}]
    db.session.commit()
    return (jsonify(return_data))


# Update Score and reset question Time
@game.route('/game/update_score')
def updateScore():
    # get the gameID from the user's browser's local memory
    gameID = get_gameID()
    game = get_game(gameID)

    # Sent the current time for the next question, and take the difference for the passed time
    previous_time = game.cr_time
    game.cr_time = datetime.now()
    passed_time = (game.cr_time.replace(tzinfo=None) - previous_time.replace(tzinfo=None))

    # Update the score based on how much time has passed.
    game.score = game.score + math.floor(float(100) * float(max(31 - passed_time.seconds, 0)) / 30)
    db.session.commit()

    return (str(game.score))


# help functions
def get_game(game_id):
    if (current_user.is_authenticated):
        print("Using game for a logged in user")
        p = Player.query.get(current_user.id)
        game = Game.query.get(p.game_id)
    else:
        print("Using game for a random user")
        game = Game.query.get(game_id)
    return game


def get_gameID():
    incomming_values = request.args.to_dict(flat=False)
    return (incomming_values.get('GameID')[0])
