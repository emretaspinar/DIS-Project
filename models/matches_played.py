from database import db_connection
from models.team import Team

class Matches_played:
    def __init__(self, round, result, opponent, team_name):
        self.round = round
        self.result = result
        self.opponent = opponent
        self.team_name = team_name

def list_matches(team_name: str):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT round, result, opponent, team_name FROM matches_played WHERE team_name = '%s';""" % team_name)
    db_matches = cur.fetchall()
    matches = []
    for db_match in db_matches:
        matches.append(Matches_played(*db_match))
    conn.close()
    return matches


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