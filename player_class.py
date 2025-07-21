import sqlite3

# Use the correct database file name!
conn = sqlite3.connect('general.db')
c = conn.cursor()
class User:
    def __init__(self, user_id=None, user_name=""):
        self.user_id = user_id
        self.user_name = user_name

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

    def login(self,user_name,user_id):
        conn = sqlite3.connect("general.db")
        c = conn.cursor()

        #c.execute('CREATE TABLE IF NOT EXISTS login(username TEXT, password TEXT)')
        # db.execute("INSERT INTO login(username, password) VALUES('admin', 'admin')")
        #c.execute("INSERT INTO login(username, password) VALUES('user', 'admin')")
        #cursor = c.cursor()

        c.execute("SELECT * FROM user where user_name=? AND user_id=?", (user_name, user_id))
        row = c.fetchone()
        if row:
           print('info', 'login success')
        else:
            print('info', 'login failed')
        c.connection.commit()
        conn.close()



#new_user = User()
#new_user.create_new_user()

sign_in_new_user = User()
sign_in_new_user.login('seniorman',2)
