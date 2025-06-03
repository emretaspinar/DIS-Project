from flask import Blueprint, render_template, request, redirect
from models.player import list_players

bp = Blueprint('player', __name__, url_prefix='/')

@bp.route('/player', methods=['GET', 'POST'])
def players():
    if request.method == 'POST':
        team_name = request.form['team_name']
        players = list_players(team_name)
        return render_template('player.html', players=players)
    else:
        return redirect('/team')

