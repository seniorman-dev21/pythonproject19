from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import math

from websockets.sync.router import route

import Realwork as rw  # module with stat list and weight dicts
from player_class import Forward, Midfielder, Defender, Goalkeeper, Everything

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions


def get_db_connection():
    conn = sqlite3.connect("general.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        user_id = request.form.get('user_id')

        if not username or not user_id:
            msg = "Please enter both username and user ID."
            return render_template('index.html', msg=msg)

        conn = sqlite3.connect("general.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_name = ? AND user_id = ?", (username, user_id))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            msg = "Incorrect username or user ID."
            return render_template('index.html', msg=msg)
    return render_template('index.html', msg=msg)

@app.route('/logged_in')
def home():
    conn = sqlite3.connect('general.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    function =cursor.execute('''
        SELECT rating.rating_id,user.user_name, player.player_name, rating.rating_value
        FROM rating
        JOIN user ON rating.user_id = user.user_id
        JOIN player ON rating.player_id = player.player_id
    ''')
    ratings = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', ratings=ratings,name=session['username'],
                           function = function)


@app.route("/delete_rating", methods=["POST"])
def delete_rating():
    rating_id = request.form['rating_id']
    print("Deleting rating_id:", rating_id)  # debug output

    conn = sqlite3.connect("general.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rating WHERE rating_id = ?", (rating_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))  # or dashboard if that’s your route


# make sure 'dashboard' exists too


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')

        conn = sqlite3.connect('general.db')
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM user WHERE user_name = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = "Username already exists!"
            user_id = existing_user[0]  # existing user_id
            conn.close()
            return render_template('register.html', msg=msg, new_id=user_id)
        else:
            cursor.execute("INSERT INTO user (user_name) VALUES (?)", (username,))
            conn.commit()
            user_id = cursor.lastrowid
            session['username'] = username
            session['user_id'] = user_id
            msg = f"Your user ID is {user_id}"
            conn.close()
            return render_template('index.html', new_id=user_id, msg=msg)


    return render_template('register.html', msg=msg, new_id=None)

@app.route("/edit_player",methods =["GET","POST"])
def edit_player():
    pass

@app.route("/create_player", methods=["GET", "POST"])
def create_player():
    from Realwork import stat
# Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    stat_dict = {}
    positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
    selected_position = None
    rating = None
    player_name = None

    if request.method == 'POST':
        # ✅ Get player name and position
        player_name = request.form.get('playername')
        selected_position = request.form.get('position')

        # ✅ Get all stat values
        for s in stat:
            value = request.form.get(s)
            if value:
                try:
                    stat_dict[s] = float(value)
                except ValueError:
                    continue  # skip invalid inputs

        # ✅ Create correct player object and calculate rating
        user = None
        if selected_position == "Forward":
            user = Forward()
        elif selected_position == "Midfielder":
            user = Midfielder()
        elif selected_position == "Defender":
            user = Defender()
        elif selected_position == "Goalkeeper":
            user = Goalkeeper()

        if user:
            user.player_name = player_name
            rating = user.get_rating(stat_dict)

            # ✅ Connect to DB
            conn = sqlite3.connect("general.db")
            cursor = conn.cursor()

            # ✅ Insert player into player table
            cursor.execute("INSERT INTO player (player_name) VALUES (?)", (player_name,))
            conn.commit()
            player_id = cursor.lastrowid

            # ✅ Store the rating
            entry = Everything(user_id=user_id, player_id=player_id, rating=rating)
            entry.store()

            # ✅ Store each stat in the submission table
            for stat_name, stat_val in stat_dict.items():
                # Lookup stat_id from stats table
                cursor.execute("SELECT stat_id FROM stats WHERE stat_name = ?", (stat_name,))
                result = cursor.fetchone()
                if result:
                    stat_id = result[0]
                    cursor.execute("""
                        INSERT INTO submission (user_id, player_id, stat_id, stat_value,rating_value)
                        VALUES (?, ?, ?, ?,?)
                    """, (user_id, player_id, stat_id, stat_val,rating))

            conn.commit()
            conn.close()

    return render_template('create_player.html',
                           stat=stat,
                           stat_dict=stat_dict,
                           selected_position=selected_position,
                           positions=positions,
                           rating=rating,
                           player_name=player_name)


if __name__ == '__main__':
    app.run(debug=True)
