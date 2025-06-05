import psycopg2
import os
import csv

# Try to get from system enviroment variable
# Set your Postgres user and password as second arguments of these two next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', '123')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    #It only works in docker if the database is called todo, we don't know why, see the comment in the dockerfile
    db = "dbname='todo' user=" + user + " host=" + host + " password =" + password # + " port = 5434"
    conn = psycopg2.connect(db)
    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()
    # We are not dropping the database before init since if you want to add the ability to add new date
    # It would be kind of stupid if that data disappeared everytime the webserver was restarted 
    cur.execute('''CREATE TABLE IF NOT EXISTS teams (team_name TEXT PRIMARY KEY, points INTEGER, wins INTEGER, losses INTEGER, draws INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS players (pid SERIAL PRIMARY KEY, player_name TEXT, nation TEXT, pos TEXT, age INTEGER, team_name TEXT, mp INTEGER, starts INTEGER, nineties FLOAT, min INTEGER, gls INTEGER, ast INTEGER, g_a INTEGER, FOREIGN KEY(team_name) REFERENCES teams(team_name))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS matches_played (round INTEGER, result TEXT, opponent TEXT, team_name TEXT, PRIMARY KEY(round, team_name), FOREIGN KEY(team_name) REFERENCES teams(team_name))''')
    conn.commit()

    with open('MatchesDataset.csv', encoding = 'UTF-8') as f:
        match_data = list(csv.DictReader(f, delimiter=';'))

    with open('PlayersDataset.csv', encoding = 'UTF-8') as f:
        player_data = list(csv.DictReader(f, delimiter=';'))

    teams = set()

    for row in player_data:
        team = row['Team']
        teams.add(team)

    for value in teams:  
        team_name_query = """
        INSERT INTO teams(team_name, points, wins, losses, draws) VALUES('%s', NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
        """ % (value)
        cur.execute(team_name_query)

    for row in player_data:
        cur.execute("""SELECT 1 FROM players WHERE player_name = '%s' AND nation = '%s' AND pos = '%s' AND age = %s AND team_name = '%s' AND mp = %s AND starts = %s AND nineties = %s AND min = %s AND gls = %s AND ast = %s AND g_a = %s """ 
        % (row['Player'], row['Nation'], row['Pos'], row['Age'], row['Team'], row['MP'], row['Starts'], row['90s'], row['Min'], row['Gls'], row['Ast'], row['G+A']))
        if cur.fetchone() is None:
            player_data_query = """
            INSERT INTO players(pid, player_name, nation, pos, age, team_name, mp, starts, nineties, min, gls, ast, g_a) VALUES(DEFAULT, '%s', '%s', '%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s ) ON CONFLICT DO NOTHING;
            """ % (row['Player'], row['Nation'], row['Pos'], row['Age'], row['Team'], row['MP'], row['Starts'], row['90s'], row['Min'], row['Gls'], row['Ast'], row['G+A'])
            cur.execute(player_data_query)

    for row in match_data:
        match_data_query = """
        INSERT INTO matches_played(round, result, opponent, team_name) VALUES(%s, '%s', '%s', '%s') ON CONFLICT DO NOTHING;
        """ % (row['Round'], row['Result'], row['Opponent'], row['Team'])
        cur.execute(match_data_query)
    
    for value in teams:
        team_results_query = """
                             UPDATE teams 
                             SET 
                             wins = 
                             (SELECT COUNT(matches_played.result)
                             FROM matches_played
                             WHERE matches_played.result = 'W' AND matches_played.team_name = '%s'),
                             losses = 
                             (SELECT COUNT(matches_played.result)
                             FROM matches_played
                             WHERE matches_played.result = 'L' AND matches_played.team_name = '%s'),
                             draws = 
                             (SELECT COUNT(matches_played.result)
                             FROM matches_played
                             WHERE matches_played.result = 'D' AND matches_played.team_name = '%s')
                             WHERE teams.team_name = '%s'; """ % (value, value, value, value)
        cur.execute(team_results_query)
        team_points_query = """
                            UPDATE teams 
                            SET 
                            points =  
                            3 * (SELECT wins FROM teams WHERE teams.team_name = '%s') + 
                            (SELECT draws FROM teams WHERE teams.team_name = '%s')
                            WHERE teams.team_name = '%s';""" % (value, value, value)
        cur.execute(team_points_query)

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
