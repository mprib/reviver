import rtoml
import reviver.logger
from dataclasses import dataclass, asdict

logger = reviver.logger.get(__name__)
from pathlib import Path
from reviver.conversation import Conversation, Message
from reviver.bot import Bot
from reviver.user import User

import sqlite3
from reviver import ROOT, SCHEMA_SQL
from pathlib import Path

class Archiver:
    def __init__(self, reviver_data_dir: Path) -> None:
        self.reviver_dir = reviver_data_dir
        self.user_id = 1 # current way I'm thinking about it, but who knows?
        self.set_db_connection()
        
    def set_db_connection(self)->sqlite3.Connection:
        self.reviver_dir.mkdir(parents=True, exist_ok=True)
    
        target_db = Path(self.reviver_dir, "reviver.db")

        if target_db.exists():
            self.conn = sqlite3.connect(target_db)
            logger.info(f"Successfull connection to database at {target_db}")
        
        else:
            # need to initialize the database
            logger.info("No previously existing database...initializing new db based on schema.sql")
            self.conn = sqlite3.connect(target_db)
            cursor = self.conn.cursor()
            cursor.executescript(SCHEMA_SQL)


    def store_bot(self, bot: Bot) -> None:
        cursor = self.conn.cursor()
        bot_data = asdict(bot)
        bot_data["user_id"] = self.user_id  # Add user_id to the dictionary

        columns = []
        placeholders = {}
        for key, value in bot_data.items():
            columns.append(key)
            placeholders[key] = value
             
        sql = f"""
            INSERT OR REPLACE INTO 
            bots 
            ({", ".join(columns)})
            VALUES 
            ({", ".join(':' + name for name in columns)})
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