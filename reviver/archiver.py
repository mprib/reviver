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
        
    def get_connection(self)->sqlite3.Connection:
        self.reviver_dir.mkdir(parents=True, exist_ok=True)
    
        target_db = Path(self.reviver_dir, "reviver.db")

        if target_db.exists():
            conn = sqlite3.connect(target_db)
            logger.info(f"Successfull connection to database at {target_db}")
        
        else:
            # need to initialize the database
            logger.info("No previously existing database...initializing new db based on schema.sql")
            conn = sqlite3.connect(target_db)
            cursor = conn.cursor()
            cursor.executescript(SCHEMA_SQL)

        return conn


    def store_bot(self, bot: Bot) -> None:
        connection = self.get_connection()
        cursor = connection.cursor()
        bot_data = asdict(bot)

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
        connection.commit()
        connection.close()

    def get_bot_list(self):
        sql = """
        SELECT bot_id from bots
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        results = cursor.execute(sql).fetchall()
        conn.close()
        bot_ids = [result[0] for result in results]
        
        return bot_ids
    
    def get_bot(self, bot_id:int)->Bot:
        sql = """
        SELECT * from bots WHERE bot_id = (:bot_id)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        results = cursor.execute(sql, {"bot_id":bot_id}).fetchall()
        conn.close()
        column_names = [description[0] for description in cursor.description]
        bot_data = {name:value for name, value in zip(column_names,results[0])}

        bot = Bot(bot_id=bot_data["bot_id"],
                  name = bot_data["name"],
                  rank=bot_data["rank"],
                  hidden=bot_data["hidden"],
                  model=bot_data["model"],
                  system_prompt=bot_data["system_prompt"],
                  max_tokens=bot_data["max_tokens"],
                  temperature=bot_data["temperature"],
                  top_p=bot_data["top_p"],
                  frequency_penalty=bot_data["frequency_penalty"],
                  presence_penalty=bot_data["presence_penalty"]
                  )

        return bot
    
    def store_user(self, user:User)->None:
        pass
    
    def get_user(self)->User:
        pass
    
    
    def store_conversation(self, convo:Conversation)->None:
        pass
    
    def get__conversation(self,convo_id)->Conversation:
        pass
