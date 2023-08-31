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
        self.user_id = 1 # current way I'm thinking about it, but who knows?
        self.set_db_connection()

        self.create_tables() # won't do anyything if they already exist
        
    def set_db_connection(self)->sqlite3.Connection:
        self.reviver_dir.mkdir(parents=True, exist_ok=True)
    
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
            model TEXT NOT NULL,
            system_prompt TEXT NOT NULL,
            max_tokens INT NOT NULL,
            temperature FLOAT NOT NULL,
            top_p FLOAT NOT NULL,
            frequency_penalty FLOAT NOT NULL,
            presence_penalty FLOAT NOT NULL,
            user_id INTEGER NOT NULL,
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


    def store_bot(self, bot: Bot) -> None:
        cursor = self.conn.cursor()
        bot_data = asdict(bot)
        bot_data["user_id"] = self.user_id  # Add user_id to the dictionary
        placeholders = {}
        for key, value in bot_data.items():
            placeholders[key] = value
             
        sql = """
            INSERT INTO bots 
            (name, model, system_prompt, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, user_id) 
            VALUES 
            (:name, :model, :system_prompt, :max_tokens, :temperature, :top_p, :frequency_penalty, :presence_penalty, :user_id)
            """
            
            
        cursor.execute(sql, placeholders)
        self.conn.commit() 
 
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

if __name__ == "__main__":
    test_bot = Bot(name = 'test_bot', model="llama70b")
    arch = Archiver(Path(ROOT, "tests", "working_delete"))

    arch.store_bot(test_bot)