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
            
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing bot data: {placeholders}")
        cursor.execute(sql, placeholders)
        connection.commit()
        connection.close()

    def get_bot_list(self):
        """
        returns a list of all bot ids stored in the database, including hidden ones
        """
        sql = """
        SELECT bot_id from bots
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute(sql).fetchall()
        conn.close()
        bot_ids = [row[0] for row in rows]
        
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
        bot = Bot(**bot_data)

        return bot
    
    def store_user(self, user:User)->None:
        user_data = asdict(user)
        columns = []
        placeholders = {}
        for key, value in user_data.items():
            columns.append(key)
            placeholders[key] = value
             
        sql = f"""
            INSERT OR REPLACE INTO 
            user
            ({", ".join(columns)})
            VALUES 
            ({", ".join(':' + name for name in columns)})
            """
            
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing user data: {placeholders}")
        cursor.execute(sql, placeholders)
        connection.commit()
        connection.close()
    
    def get_user(self)->User:
        """
        Current data schema only has one user....
        """
        sql = """
        SELECT * from user
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        rows = cursor.execute(sql).fetchall()
        column_names = [description[0] for description in cursor.description]
        user_data = {name:value for name, value in zip(column_names,rows[0])}
        user = User(**user_data)
        conn.close()
        return user

    def store_messages(self, messages:dict[int, Message])->None:
        for position, msg in messages.items():
            self.store_message(msg)
            
    def get_messages(self, conversation_id:int)-> dict[int,Message]:
        
        # need to get all message positions first
        sql = """
        SELECT position FROM messages WHERE conversation_id = :conversation_id
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        rows = cursor.execute(sql, {"conversation_id":conversation_id}).fetchall()

        msg_positions = [position[0] for position in rows]
        
        logger.info(f"Message positions are:{msg_positions}")

        messages = {position:self.get_message(conversation_id, position) for position in msg_positions}
        
        return messages
        
    def store_message(self,message:Message)->None:
        message_data = asdict(message)
        columns = []
        placeholders = {}
        for key, value in message_data.items():
            columns.append(key)
            placeholders[key] = value
             
        sql = f"""
            INSERT OR REPLACE INTO 
            messages
            ({", ".join(columns)})
            VALUES 
            ({", ".join(':' + name for name in columns)})
            """
            
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing message data: {placeholders}")
        cursor.execute(sql, placeholders)
        connection.commit()
        connection.close()

    def get_message(self,conversation_id:int, position:int)->Message:
        sql = """
        SELECT * FROM messages WHERE conversation_id=? AND position =?
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        rows = cursor.execute(sql, (conversation_id, position)).fetchall()
        column_names = [description[0] for description in cursor.description]
        msg_data = {name:value for name, value in zip(column_names,rows[0])}
        conn.close()
        msg = Message(**msg_data)
        return msg
    
    def store_conversation(self, convo:Conversation)->None:
        pass
    
    def get__conversation(self,convo_id)->Conversation:
        pass
