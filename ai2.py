import sqlite3


conn= sqlite3.connect("general.db")
c= conn.cursor()
user_id = 1

c.execute( "SELECT * FROM user where user_id=?",
           (user_id,))
row = c.fetchone()[1]

player_id = 1
c.execute( "SELECT * FROM player where player_id=?",
           (player_id,))
row1 = c.fetchone()[1]

stat_id = 5
c.execute("SELECT stat_value FROM submission WHERE stat_id = ?", (stat_id,))
row3 = c.fetchone()


player_id = 1
user_id = 1
c.execute("SELECT rating_value FROM rating WHERE user_id = ? AND player_id = ?", (user_id, player_id))
row4 = c.fetchone()[0]

stat_id = 5
for stat in range(stat_id):
    c.execute("SELECT * FROM stats WHERE stat_id = ?", (stat,))
    row2 = c.fetchone()
    if row2:  # Check if a row was found
        row2 = row2[1]
        #print(row2)
        print(
            f"{row} rated a player called {row1} his value for {row2} is stored as {row3} with a final rating of {row4}")


print(f"{row} rated a player called {row1} his value for {row2} is stored as {row3} with a final rating of {row4}")