# IS496: Computer Networks
# Course Mini-Project
# Name and Netid of each member:
# Member 1: chenzhao wang, cw107
# Member 2: Zhen Li, zhenli6
import sqlite3

DATABASE_FILENAME = 'FilmFinder.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILENAME)
    conn.row_factory = sqlite3.Row  
    return conn