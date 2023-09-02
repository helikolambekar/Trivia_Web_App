from source.models import Game, Question, Player, LeaderboardScore


# Test for the game session object
def test_game_model():
    game = Game(type='TEST', lives=3, score=0, question_time=30,
                num_skip_question=3, questions_left=str(0),
                answer_location=0, max_questions=0)
    # This portion ensures that all of the functional aspects of the game table were actively updated.
    assert game.lives == 3
    assert game.score == 0
    assert game.question_time == 30
    assert game.num_skip_question == 3
    assert game.max_questions == 0
    assert game.answer_location == 0
    assert game.questions_left == '0'



# Test for the player object
def test_Player_Model():
    player = Player(email="test@gmail.com", password="1234567", player_name="TestPlayer")
    assert player.email == "test@gmail.com"
    assert player.password == "1234567"
    assert player.player_name == "TestPlayer"

# Test for the question object
def test_Question_model():
    questions = Question(
        category='test_category',
        question='test_question',
        answer='test_answer',
        option_1='test_option_1',
        option_2='test_option_2',
        option_3='test_option_3'
    )
    assert questions.category == 'test_category'
    assert questions.question == 'test_question'
    assert questions.answer == 'test_answer'
    assert questions.option_1 == 'test_option_1'
    assert questions.option_2 == 'test_option_2'
    assert questions.option_3 == 'test_option_3'


# Test for the ledaerboard object
def test_LeaderboardScore_model():
    leaderboard = LeaderboardScore(
        category='categoryTest',
        username='userNameTest',
        score=1000
    )

    assert leaderboard.score == 1000
    assert leaderboard.category == 'categoryTest'
    assert leaderboard.username == 'userNameTest'
