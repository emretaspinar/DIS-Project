import psycopg2
import os
import pandas as pd

# Try to get from system enviroment variable
# Set your Postgres user and password as second arguments of these two next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', '123')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    db = "dbname='EPL' user=" + user + " host=" + host + " password =" + password
    conn = psycopg2.connect(db)

    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS teams (team_name TEXT PRIMARY KEY, points INTEGER, wins INTEGER, losses INTEGER, draws INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS players (pid SERIAL PRIMARY KEY, player_name TEXT, nation TEXT, age INTEGER, team_name TEXT, FOREIGN KEY(team_name) REFERENCES teams(team_name))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS matches_played (round INTEGER, result TEXT, opponent TEXT, team_name TEXT, PRIMARY KEY(round, team_name), FOREIGN KEY(team_name) REFERENCES teams(team_name))''')
    conn.commit()

    with open('MatchesDataset.csv', encoding = 'UTF-8') as f:
        match_data = pd.read_csv(f, delimiter=';')
    

    with open('PlayersDataset.csv', encoding = 'UTF-8') as f:
        player_data = pd.read_csv(f, delimiter=';')

    for value in player_data['Team'].unique():  
        team_name_query = """
        INSERT INTO teams(team_name, points, wins, losses, draws) VALUES('%s', NULL, NULL, NULL, NULL);
        """ % (value)
        cur.execute(team_name_query)

    for row in player_data.to_dict('records'):
        player_data_query = """
        INSERT INTO players(pid, player_name, nation, age, team_name) VALUES(DEFAULT, '%s', '%s', %i, '%s');
        """ % (row['Player'], row['Nation'], row['Age'], row['Team'])
        cur.execute(player_data_query)

    for row in match_data.to_dict('records'):
        match_data_query = """
        INSERT INTO matches_played(round, result, opponent, team_name) VALUES('%i', '%s', '%s', '%s');
        """ % (row['Round'], row['Result'], row['Opponent'], row['Team'])
        cur.execute(match_data_query)
    



    '''
    categories = ['DIS', 'House chores']
    for category in categories:
        cur.execute('INSERT INTO categories (category_name) VALUES (%s) ON CONFLICT DO NOTHING', (category,))

    todos = [('Assignment 1', 'DIS'), ('Groceries', 'House chores'), ('Assignment 2', 'DIS'), ('Project', 'DIS')]
    for (todo, category) in todos:
        cur.execute('INSERT INTO todos (todo_text, category_id) VALUES (%s, (SELECT id FROM categories WHERE category_name = %s)) ON CONFLICT DO NOTHING', (todo, category))
    '''
    conn.commit()
    conn.close()
