import sqlite3

conn = sqlite3.connect('general.db')
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON;")

# Create user table

# 1. User table
c.execute("""
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL
)
""")

# 2. Create the player table
c.execute("""
CREATE TABLE IF NOT EXISTS player (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL
)
""")

# 3. Create the rating table
c.execute("""
CREATE TABLE IF NOT EXISTS rating (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    rating_value REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id))
    
""")

c.execute("""
CREATE TABLE IF NOT EXISTS stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_name TEXT NOT NULL)

""")

c.execute("""
CREATE TABLE IF NOT EXISTS submission (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    stat_id INTEGER NOT NULL,
    stat_value INTEGER NOT NULL,
    time TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (stat_id) REFERENCES stats(stat_id)
)
""")




conn.commit()
conn.close()



