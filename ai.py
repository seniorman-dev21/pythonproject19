import sqlite3
conn = sqlite3.connect('general.db')
c = conn.cursor()
from Realwork import stat
def insert_stat(stats):
    data = [(s,) for s in stats]  # Convert to list of 1-element tuples
    c.executemany("INSERT INTO stats (stat_value) VALUES (?)", data)
    conn.commit()



insert_stat(stat)
num = [('defender',1),
        ('forward',2),
      ('midfielder',3),
       ('goalkeeper' ,4)]
#c.executemany("INSERT INTO position (position_name,position_id) VAlUES (?,?)",num)
#conn.commit()
#conn.close()

def rating():
        positions = input("""please select a position,
        forward
        defender
        midfielder
        goalkeeper:""").strip().lower()
        c.execute("SELECT * FROM position where position_name=?", (positions,))
        row = c.fetchone()
        if row:
           print('info', 'login success')
        else:
            print('info', 'login failed')
        conn.commit()
        conn.close()

#rating()
def insert_data_into_database():
     c.execute("SELECT position_id FROM position")
     poss = c.fetchall()
     c.execute("SELECT stat_id FROM stat")
     pos=c.fetchall()
     #print(pos)
     for each_poss in poss:
         for each_pos in pos:
             c.execute("INSERT INTO rating_weights (position_id, stat_id) VALUES (?, ?)", (each_poss[0], each_pos[0]))

     conn.commit()


    


def display_valid_stat_and_calculate_rating():
    c.execute("SELECT stat_name FROM stat")
    c.execute ("SELECT ")



#display_valid_stat_and_calculate_rating()
#insert_data_into_database()