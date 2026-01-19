import sqlite3
import Realwork as rw
import math
# Use the correct database file name!
conn = sqlite3.connect('general.db')
c = conn.cursor()
class Account:
    def __init__(self):
        self.user_id = None
        self.user_name = ""

    def create_new_user(self):
        self.user_name = input("Please enter your name: ")
        print(f"Thank you, your user name is now {self.user_name}.")

        # Insert into user table only
        c.execute("INSERT INTO user (user_name) VALUES (?)",
                  (self.user_name,))

        conn.commit()

        self.user_id = c.lastrowid
        print(f"User added with ID: {self.user_id}")
        return self.user_name

    def login(self):
        """logs users in if already signed in"""
        #conn = sqlite3.connect("general.db")
        #c = conn.cursor()

        #c.execute('CREATE TABLE IF NOT EXISTS login(username TEXT, password TEXT)')
        # db.execute("INSERT INTO login(username, password) VALUES('admin', 'admin')")
        #c.execute("INSERT INTO login(username, password) VALUES('user', 'admin')")
        #cursor = c.cursor()

        c.execute("SELECT * FROM user where user_name=? AND user_id=?", (self.user_name, self.user_id))
        row = c.fetchone()
        if row:
           print('info', 'login success')
        else:
            print('info', 'login failed')
        c.connection.commit()
        #conn.close()



class User:
    def __init__(self):
        self.stats = []
        self.player_name = ""
        self.player_id = None
        self.stat_value = {}

    def input_stats(self):
        import Realwork as rw
        stat_value = {}
        for each_stat in rw.stat:
            num =input(f"Please enter a value for {each_stat}")
            stat_value[each_stat] = float(num)
        return stat_value

    def create_a_new_player(self):
        self.player_name = input("Please enter a player name: ")
        print(f"Thank you, the player name is now {self.player_name}.")

        # Insert into user table only
        c.execute("INSERT INTO player (player_name) VALUES (?)",
                  (self.player_name,))

        conn.commit()

        self.player_id = c.lastrowid
        print(f"User added with ID: {self.player_id}")
        return self.player_name

class Player:
    def __init__(self):
        self.stat_value = {}
        self.player_name = ""
        self.player_id = None


class Forward(Player):
    def get_rating(self,stat_value):
        self.stat_value = stat_value
        rating = 0
        for key, weight in rw.FORWARD_STATS.items():
            rating += weight * stat_value.get(key, 0)
        return rating

class Midfielder(Player):
    def get_rating(self,stat_value):
        self.stat_value = stat_value
        rating = 0
        for key, weight in rw.MIDFIELDER_STATS.items():
            rating += weight * stat_value.get(key, 0)
        return rating


class Defender(Player):
    def get_rating(self,stat_value):
        self.stat_value = stat_value
        rating = 0
        for key, weight in rw.DEFENDER_STATS.items():
            rating += weight * stat_value.get(key, 0)
        return rating

class Goalkeeper(Player):
    def get_rating(self,stat_value):
        self.stat_value = stat_value
        rating = 0
        for key, weight in rw.GOALKEEPER_STATS.items():
            rating += weight * stat_value.get(key, 0)
        return rating

class Everything:
    def __init__(self,user_id,player_id,rating):
        self.user_id = user_id
        self.player_id = player_id
        self.rating = rating

    def store(self):
        conn = sqlite3.connect("general.db")
        c = conn.cursor()

        c.execute("SELECT * FROM player where player_id=?", (self.player_id,))
        row = c.fetchone()
        c.execute("SELECT * FROM user where user_id=?", (self.user_id,))
        row2 = c.fetchone()
        c.execute("INSERT INTO rating (user_id, player_id,rating_value) VALUES (?, ?,?)",
                  (row2[0],row[0],self.rating ))
        conn.commit()






#user =Everything(1,1,100)
#user.store()

def main():
    print("Welcome to the Player Rating System")
    acc = Account()

    choice = input("Do you want to (1) Create a new user or (2) Log in? Enter 1 or 2: ")

    if choice == "1":
        acc.create_new_user()
    elif choice == "2":
        acc.user_name = input("Enter your username: ")
        acc.user_id = int(input("Enter your user ID: "))
        acc.login()
    else:
        print("Invalid choice.")
        return

    user = User()
    player_name = user.create_a_new_player()
    stat_values = user.input_stats()

    print("Select player position:")
    print("1. Forward")
    print("2. Midfielder")
    print("3. Defender")
    print("4. Goalkeeper")
    position_choice = input("Enter choice (1-4): ")

    if position_choice == "1":
        player = Forward()
    elif position_choice == "2":
        player = Midfielder()
    elif position_choice == "3":
        player = Defender()
    elif position_choice == "4":
        player = Goalkeeper()
    else:
        print("Invalid position selected.")
        return

    rating = player.get_rating(stat_values)
    print(f"{player_name}'s rating as a {player.__class__.__name__}: {rating:.2f}")

    everything = Everything(acc.user_id, user.player_id, rating)
    everything.store()


if __name__ == "__main__":
    main()

conn.close()
print(1)









