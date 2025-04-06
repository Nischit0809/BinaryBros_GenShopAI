import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        with open(os.path.join(os.path.dirname(__file__), 'init_db.sql'), 'r') as f:
            conn.executescript(f.read())

def save_chat_memory(user_id, message, response):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chat_memory (user_id, message, response) VALUES (?, ?, ?)",
            (user_id, message, response)
        )
        conn.commit()

def fetch_user_chats(user_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT message, response, timestamp FROM chat_memory WHERE user_id = ? ORDER BY timestamp DESC",
            (user_id,)
        )
        return cursor.fetchall()
