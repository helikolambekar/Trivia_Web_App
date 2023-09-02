from flask import Blueprint, redirect, url_for
from flask_login.utils import login_required

from . import db
from .models import LeaderboardScore, Game, Player
from flask_login import current_user

leaderboard = Blueprint('leaderboard', __name__)


@leaderboard.route('/leaderboard/create', methods=['POST'])
@login_required
def leaderBoard_create():
    p = Player.query.get(current_user.id)
    game = Game.query.get(p.game_id)
    username = current_user.player_name
    score = game.score
    userid = current_user.id if current_user.is_authenticated else 0
    new_score = LeaderboardScore(category=game.category, userid=userid, username=username, score=score)
    db.session.add(new_score)
    db.session.commit()
    return redirect(url_for('views.leaderBoard'))
