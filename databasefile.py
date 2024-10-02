import sqlite3

# Connect to the SQLite database (it will create the file if it doesn’t exist)
conn = sqlite3.connect('real_madrid.db')
cursor = conn.cursor()

# Create the players table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jersey_number INTEGER NOT NULL UNIQUE,
        player_name TEXT NOT NULL,
        position TEXT,
        age INTEGER,
        goals INTEGER DEFAULT 0,
        assists INTEGER DEFAULT 0,
        matches_played INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def insert_player(jersey_number=1, player_name='Thibaut Courtois', position='GK', age=32, goals=0, assists=0, matches_played=0):
    query = """
    INSERT INTO players (jersey_number, player_name, position, age, goals, assists, matches_played)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (jersey_number, player_name, position, age, goals, assists, matches_played))
    conn.commit()

