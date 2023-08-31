import rtoml
import reviver.logger
from dataclasses import dataclass, asdict

logger = reviver.logger.get(__name__)
from pathlib import Path
from reviver.conversation import Conversation, Message
from reviver.bot import Bot
from reviver.user import User

import sqlite3
from reviver import ROOT
from pathlib import Path

class Archiver:
    def __init__(self, reviver_dir: Path) -> None:
        self.reviver_dir = reviver_dir
        self.set_db_connection()

        self.create_tables() # won't do anyything if they already exist
        
    def set_db_connection(self)->sqlite3.Connection:
    
        target_db = Path(self.reviver_dir, "reviver.db")
        try:
            self.conn = sqlite3.connect(target_db)
            logger.info(f"Successfull connection to database at {target_db}")
        except:
            logger.info(f"Unable to create or load db from {str(target_db)}")


    def create_tables(self):
        cursor = self.conn.cursor()

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


    def store_bot(self,bot:Bot)->None:
        pass
    
    def get_bot(self, bot_id:int)->Bot:
        pass
    
    
    def store_user(self, user:User)->None:
        pass
    
    def get_user(self)->User:
        pass
    
    
    def store_conversation(self, convo:Conversation)->None:
        pass
    
    def get__conversation(self,convo_id)->Conversation:
        pass