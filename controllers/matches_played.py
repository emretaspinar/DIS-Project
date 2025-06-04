from flask import Blueprint, render_template, request, redirect
from models.matches_played import list_matches

bp = Blueprint('matches_played', __name__, url_prefix='/')

@bp.route('/matches_played', methods=['GET', 'POST'])
def matches_played():
    if request.method == 'POST':
        team_name = request.form['team_name']
        print(team_name)
        matches_played = list_matches(team_name)
        return render_template('matches_played.html', matches_played=matches_played)
    else:
        return redirect('/team')