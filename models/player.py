from database import db_connection
from models.team import Team

class Player:
    def __init__(self, pid, player_name, nation, age, team_name):
        self.pid = pid
        self.player_name = player_name
        self.nation = nation
        self.age = age
        self.team_name = team_name

def list_players(team_name: str):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT pid, player_name, nation, age, team_name FROM players WHERE team_name = '%s';""" % team_name)
    db_players = cur.fetchall()
    players = []
    for db_player in db_players:
        players.append(Player(db_player[0], db_player[1], db_player[2], db_player[3], db_player[4]))
    conn.close()
    return players

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