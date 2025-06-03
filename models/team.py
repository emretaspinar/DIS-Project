import pandas as pd
from database import db_connection

class Team:
    def __init__(self, team_name, points, wins, losses, draws):
        self.team_name = team_name
        self.points = points
        self.wins = wins
        self.losses = losses
        self.draws = draws

def list_teams():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT team_name, points, wins, losses, draws FROM teams')
    db_teams = cur.fetchall()
    teams = []
    for db_team in db_teams:
        teams.append(Team(db_team[0], db_team[1], db_team[2], db_team[3], db_team[4]))
    conn.close()
    return teams

'''
def list_todos():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT todos.id as tid, todo_text, categories.id as cid, category_name FROM todos JOIN categories ON todos.category_id = categories.id')
    db_todos = cur.fetchall()
    todos = []
    for db_todo in db_todos:
        todos.append(Todo(db_todo[0], db_todo[1], Category(db_todo[2], db_todo[3])))

    conn.close()
    return todos
'''

'''
def insert_todo(text, category_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (todo_text, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (text, category_id))
    cur.close()
    conn.commit()
    conn.close()
'''