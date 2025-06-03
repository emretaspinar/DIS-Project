from flask import Blueprint, render_template, request
from models.team import list_teams

bp = Blueprint('team', __name__, url_prefix='/')

@bp.route('/team', methods=['GET', 'POST'])
def teams():
    teams = list_teams()

    return render_template('team.html', teams=teams)
