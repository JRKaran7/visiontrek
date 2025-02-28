import sqlite3

def init_db():
    conn = sqlite3.connect("database/scores.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, points INTEGER)''')
    conn.commit()
    conn.close()

def save_score(points):
    conn = sqlite3.connect("database/scores.db")
    c = conn.cursor()
    c.execute("INSERT INTO scores (points) VALUES (?)", (points,))
    conn.commit()
    conn.close()

def get_high_score():
    conn = sqlite3.connect("database/scores.db")
    c = conn.cursor()
    c.execute("SELECT MAX(points) FROM scores")
    result = c.fetchone()[0]
    conn.close()
    return result if result else 0
