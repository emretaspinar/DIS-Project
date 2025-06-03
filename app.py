from flask import Flask, redirect
from database import init_db
from controllers import team, player

init_db()

app = Flask(__name__)

@app.route("/")
def home():
    return redirect('/team')

app.register_blueprint(team.bp)
app.register_blueprint(player.bp)
