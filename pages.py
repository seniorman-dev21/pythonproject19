import sqlite3
def update():
    conn = sqlite3.connect("general.db")
    c= conn.cursor()
    player_id = 59
    c.execute("""SELECT submission.stat_value,
            stats.stat_name FROM submission
            JOIN stats ON submission.stat_id = stats.stat_id
            WHERE submission.player_id = ?""", (player_id,))
    x = c.fetchall()
    new_stats = {stat_name: value for value, stat_name in x}
    print(x)
    print(new_stats)
    new_stats['Age'] = 12
    print(new_stats)
    for stat_name, value in new_stats.items():
        c.execute("""
            UPDATE submission
            SET stat_value = ?
            WHERE player_id = ? AND stat_id = (
                SELECT stat_id FROM stats WHERE stat_name = ?
            )
        """, (value, player_id, stat_name))

    player_id = 59
    c.execute("""SELECT submission.stat_value,
            stats.stat_name FROM submission
            JOIN stats ON submission.stat_id = stats.stat_id
            WHERE submission.player_id = ?""", (player_id,))
    x = c.fetchall()
    new_stats = {stat_name: value for value, stat_name in x}
    print(x)
    conn.commit()
