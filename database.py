import psycopg2
import os
import pandas as pd

# Try to get from system enviroment variable
# Set your Postgres user and password as second arguments of these two next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', '2003')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    db = "dbname='EPL' user=" + user + " host=" + host + " password =" + password + " port = 5434"
    conn = psycopg2.connect(db)

    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS teams (team_name TEXT PRIMARY KEY, points INTEGER, wins INTEGER, losses INTEGER, draws INTEGER)''')
    cur.execute('DROP TABLE IF EXISTS players CASCADE;')
    cur.execute('''CREATE TABLE IF NOT EXISTS players (pid SERIAL PRIMARY KEY, player_name TEXT, nation TEXT, pos TEXT, age INTEGER, team_name TEXT, mp INTEGER, starts INTEGER, nineties FLOAT, min INTEGER, gls INTEGER, ast INTEGER, g_a INTEGER, FOREIGN KEY(team_name) REFERENCES teams(team_name))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS matches_played (round INTEGER, result TEXT, opponent TEXT, team_name TEXT, PRIMARY KEY(round, team_name), FOREIGN KEY(team_name) REFERENCES teams(team_name))''')
    conn.commit()

    with open('MatchesDataset.csv', encoding = 'UTF-8') as f:
        match_data = pd.read_csv(f, delimiter=';')
    

    with open('PlayersDataset.csv', encoding = 'UTF-8') as f:
        player_data = pd.read_csv(f, delimiter=';')
        player_data.rename(columns={'90s': 'nineties'}, inplace=True)

    with open('AdvancedStatsDataset.csv', encoding = 'UTF-8') as f:
        Stats_data = pd.read_csv(f, delimiter=';')


    for value in player_data['Team'].unique():  
        team_name_query = """
        INSERT INTO teams(team_name, points, wins, losses, draws) VALUES('%s', NULL, NULL, NULL, NULL) ON CONFLICT DO NOTHING;
        """ % (value)
        cur.execute(team_name_query)

    for record in player_data.to_dict('records'):
        cur.execute("""SELECT 1 FROM players WHERE player_name = '%s' AND nation = '%s' AND pos = '%s' AND age = %i AND team_name = '%s' AND mp = %i AND starts = %i AND nineties = %f AND min = %i AND gls = %i AND ast = %i AND g_a = %i """ 
        % (record['Player'], record['Nation'], record['Pos'], record['Age'], record['Team'], record['MP'], record['Starts'], record['nineties'], record['Min'], record['Gls'], record['Ast'], record['G+A']))
        if cur.fetchone() is None:
            player_data_query = """
            INSERT INTO players(pid, player_name, nation, pos, age, team_name, mp, starts, nineties, min, gls, ast, g_a) VALUES(DEFAULT, '%s', '%s', '%s', '%i', '%s', '%i', '%i', '%f', '%i', '%i', '%i', '%i' ) ON CONFLICT DO NOTHING;
            """ % (record['Player'], record['Nation'], record['Pos'], record['Age'], record['Team'], record['MP'], record['Starts'], record['nineties'], record['Min'], record['Gls'], record['Ast'], record['G+A'])
            cur.execute(player_data_query)

    for record in match_data.to_dict('records'):
        match_data_query = """
        INSERT INTO matches_played(round, result, opponent, team_name) VALUES('%i', '%s', '%s', '%s') ON CONFLICT DO NOTHING;
        """ % (record['Round'], record['Result'], record['Opponent'], record['Team'])
        cur.execute(match_data_query)
    
    cur.execute("""SELECT team_name FROM teams""")
    team_names = pd.DataFrame(cur.fetchall(), columns=['team_name'])
    for record in team_names.to_dict('records'):
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
                             WHERE teams.team_name = '%s'; """ % (record['team_name'], record['team_name'], record['team_name'], record['team_name'])
        cur.execute(team_results_query)
        team_points_query = """
                            UPDATE teams 
                            SET 
                            points =  
                            3 * (SELECT wins FROM teams WHERE teams.team_name = '%s') + 
                            (SELECT draws FROM teams WHERE teams.team_name = '%s')
                            WHERE teams.team_name = '%s';""" % (record['team_name'], record['team_name'], record['team_name'])
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
