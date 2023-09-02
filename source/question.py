from flask import Blueprint, jsonify
import random
from datetime import datetime
from . import db
from .models import Question
from .game import get_gameID, get_game

question = Blueprint('question', __name__)


@question.route('/question/')
def getSingleQuestion():
    # get the gameID from the user's browser's local memory
    gameID = get_gameID()
    game = get_game(gameID)

    # get random question from ID's remaining
    questions_left = game.questions_left.split(',')

    print("QUESTIONS LEFT:" + str(questions_left))
    if len(questions_left)== 1:
       questions_left = reset_questions(game)
       questions_left = questions_left.split(',')
    # sets weather heavy-filter needs to be used or not
    heavy_filter = True

    # the first question has a [ at the beginning which needs to be removed, only when the list wasn't just re-initialized.
    if heavy_filter == True:
        str_id = int(''.join(filter(str.isdigit, questions_left[0])))
    else:
        str_id = questions_left[0]
    questions_left.remove(questions_left[0])
    print(str_id)
    q = Question.query.get(str_id)
    print(q.question)

    # Shuffle the 4 potential answers
    answer_location = 0
    input = [q.answer, q.option_1, q.option_2, q.option_3]
    answers = random.sample(input, len(input))

    # Determine the location of the answer
    for x in range(4):
        if answers[x] == q.answer:
            answer_location = x + 1

    # clean up the questions_left string into just ints, for some reason it grows otherwise
    for i in range(0, len(questions_left)):
        if (i < len(questions_left) - 1):
            questions_left[i] = int(questions_left[i])
        else:
            # the last question has a ] at the end which needs to be removed
            questions_left[i] = int(questions_left[i].rstrip(questions_left[i][-1]))

    # This will also have to reinitialize just the questions related to the category so the same logic utilized in game.py will need to be used here
    # if the questions_left array is empty, reinitialize it with all of the questions.
    if len(questions_left) == 0:
        heavy_filter = False
        if game.category == '':
            questions_left = random.sample(list(range(1, game.max_questions + 1)), game.max_questions)
        else:
            for k in range(game.max_questions):
                j = Question.query.get(k + 1)
                if j.category == game.category:
                    questions_left.append(j.id)
            questions_left = random.sample(questions_left, len(questions_left))

    # Update all of these parameters in the game object, including the game time
    # TODO I need to remove the question details from the game object and just store the question primary key
    game.questions_left = str(questions_left)
    print(game.questions_left)
    game.question = q.id
    game.answer_location = answer_location
    game.cr_time = datetime.now()
    db.session.commit()

    # convert data into JSON object
    return_data = [{"Question": q.question}, {"Option_1": answers[0]}, {"Option_2": answers[1]},
                   {"Option_3": answers[2]}, {"Option_4": answers[3]}]

    # print data to be retuned on back end
    print(return_data)
    # return data as json
    return jsonify(return_data)

def reset_questions(game):
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

        ("FILTRED QUESTION IDs:")
        print(questions_left)
        return(str(questions_left))