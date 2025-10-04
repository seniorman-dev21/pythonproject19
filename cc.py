from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pandas as pd
from player_class import Forward, Midfielder, Defender, Goalkeeper, Everything

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/create_players_auto", methods=["GET", "POST"])
def create_players_auto():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    stat_list = [
        "Age","Appearances","Losses","Goals","Penalties scored","Freekicks scored","Shots","Shots on target",
        "Hit woodwork","Clean sheets","Goals conceded","Tackles","Blocked shots","Interceptions",
        "Clearances","Headed Clearance","Clearances off line","Recoveries","Duels won",
        "Successful 50/50s","Aerial battles won","Own goals","Assists","Passes",
        "Crosses","Through balls","Accurate long balls","Saves",
        "Penalties saved","Punches","High Claims","Catches","Sweeper clearances","Throw outs",
        "Goal Kicks","Yellow cards","Fouls","Offsides"
    ]

    ratings_generated = []

    if request.method == "POST":
        # Uploaded CSV file
        file = request.files.get("player_csv")
        if not file:
            return "No file uploaded", 400

        try:
            df = pd.read_csv(file)
        except Exception as e:
            return f"Error reading CSV file: {e}", 400

        conn = sqlite3.connect("general.db")
        cursor = conn.cursor()

        for _, row in df.iterrows():
            player_name = row.get("Name")  # Match your CSV column
            position = row.get("Position")

            # Skip rows with missing player name or position
            if not player_name or str(player_name).strip() == "":
                continue
            if not position or str(position).strip() == "":
                continue

            # Build stat dictionary, ignore extra columns

            stat_dict = {
                s: float(str(row[s]).replace(',', '').rstrip('%')) if s in row and pd.notna(row[s]) else 0
                for s in stat_list
            }

            # Create appropriate player object
            player_obj = None
            if position == "Forward":
                player_obj = Forward()
            elif position == "Midfielder":
                player_obj = Midfielder()
            elif position == "Defender":
                player_obj = Defender()
            elif position == "Goalkeeper":
                player_obj = Goalkeeper()
            if not player_obj:
                continue

            player_obj.player_name = player_name
            rating = player_obj.get_rating(stat_dict)

            # Insert player
            cursor.execute("INSERT INTO player (player_name) VALUES (?)", (player_name,))
            conn.commit()
            player_id = cursor.lastrowid

            # Store rating
            entry = Everything(user_id=user_id, player_id=player_id, rating=rating)
            entry.store()

            # Store individual stats
            for stat_name, stat_val in stat_dict.items():
                cursor.execute("SELECT stat_id FROM stats WHERE stat_name = ?", (stat_name,))
                result = cursor.fetchone()
                if result:
                    stat_id = result[0]
                    cursor.execute("""
                        INSERT INTO submission (user_id, player_id, stat_id, stat_value, rating_value)
                        VALUES (?, ?, ?, ?, ?)
                    """, (user_id, player_id, stat_id, stat_val, rating))

            ratings_generated.append((player_name, rating))

        conn.commit()
        conn.close()

        # Render dashboard or results page with generated ratings
        return redirect(url_for("home", rating_value=ratings_generated))

    return render_template("create_players_auto.html")




