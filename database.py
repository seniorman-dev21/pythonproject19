import sqlite3

conn = sqlite3.connect('general.db')
c= conn.cursor()

#c.execute("PRAGMA foreign_keys = ON;")

command1 = """CREATE TABLE IF NOT EXISTS
user(user_id INTEGER PRIMARY KEY,user_name TEXT) """
c.execute(command1)

command2 = """CREATE TABLE IF NOT EXISTS
player(player_id INTEGER PRIMARY KEY,player_name TEXT,user_id INTEGER,rating FLOAT,
FOREIGN KEY(user_id) REFERENCES user(user_id))"""
c.execute(command2)

command3 = """CREATE TABLE IF NOT EXISTS
stat_type(stat_type_id INTEGER PRIMARY KEY,stat_name TEXT)"""
c.execute(command3)

command4 = """CREATE TABLE IF NOT EXISTS
statistics(stat_id INTEGER PRIMARY KEY,player_id INTEGER,
user_id INTEGER,stat_type_id INTEGER,
stat_value FLOAT ,weighting FLOAT,
FOREIGN KEY(user_id) REFERENCES user(user_id),
FOREIGN KEY(player_id) REFERENCES player(player_id),
FOREIGN KEY(stat_type_id) REFERENCES stat_type(stat_type_id))"""
c.execute(command4)





