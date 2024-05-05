# IS496: Computer Networks
# Course Mini-Project
# Name and Netid of each member:
# Member 1: chenzhao wang, cw107
# Member 2: Zhen Li, zhenli6
from .database import get_db_connection

def register_user(user_name, password):
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO User (user_name, password) VALUES (?, ?)",
            (user_name, password)
        )
        conn.commit()
    return True

def check_user_cred(user_name, password):
    with get_db_connection() as conn:
        user = conn.execute(
            "SELECT * FROM User WHERE user_name = ?", (user_name,)
        ).fetchone()
        if user and user['password'] == password:
            return True
    return False

def get_user_id(user_name, password):
    with get_db_connection() as conn:
        result = conn.execute(
            "SELECT user_id FROM User WHERE user_name = ? AND password = ?", (user_name, password)
        ).fetchone()
    return result['user_id']

def is_username_available(user_name):
    with get_db_connection() as conn:
        result = conn.execute(
            "SELECT user_name FROM User WHERE user_name = ?", (user_name,)
        ).fetchone()
        if result:
            return False
        else:
            return True
