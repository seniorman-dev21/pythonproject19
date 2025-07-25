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

conn.commit()
conn.close()



import sqlite3

def show_all_users(db_file='general.db'):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Make sure the user table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
    if not c.fetchone():
        print("No 'user' table found in the database.")
        conn.close()
        return

    # Fetch and display all users
    c.execute("SELECT user_id, user_name FROM user")
    rows = c.fetchall()

    if rows:
        print("List of users:")
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}")
    else:
        print("No users found in the database.")

    conn.close()

# Call the function
show_all_users()
