
import reviver.logger
logger = reviver.logger.get(__name__)

import sqlite3
from reviver import ROOT
from pathlib import Path



def get_conn(user_path:Path):
    
    target_db = Path(user_path, "reviver.db")
    try:
        conn = sqlite3.connect(target_db)
        logger.info(f"Successfull connection to database at {target_db}")
    except:
        logger.info(f"Unable to create or load db from {str(target_db)}")

    return conn

def create_tables(conn:sqlite3.Connection):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        key_path TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        bot_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY(bot_id) REFERENCES bots(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        time TIMESTAMP NOT NULL,
        role TEXT NOT NULL,
        conversation_id INTEGER,
        FOREIGN KEY(conversation_id) REFERENCES conversations(id)
    );
    """)

if __name__ == "__main__":
    test_user_dir = Path(ROOT, "tests", "working_delete")
    conn = get_conn(test_user_dir)
    create_tables(conn) 
    