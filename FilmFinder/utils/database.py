import sqlite3

DATABASE_FILENAME = 'FilmFinder.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILENAME)
    conn.row_factory = sqlite3.Row  
    return conn