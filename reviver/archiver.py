import reviver.logger
from dataclasses import asdict

from pathlib import Path
from reviver.conversation import Conversation, Message

from reviver.bot import Bot, BotGallery
from reviver.user import User

import sqlite3
from reviver import SCHEMA_SQL

logger = reviver.logger.get(__name__)

class Archive:
    def __init__(self, reviver_data_dir: Path) -> None:
        self.reviver_dir = reviver_data_dir
        self.user_id = 1 # current way I'm thinking about it, but who knows?
        self.get_connection()
        
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
        bindings = {}
        for key, value in bot_data.items():
            columns.append(key)
            bindings[key] = value
             
        sql = f"""
            INSERT OR REPLACE INTO 
            bots 
            ({", ".join(columns)})
            VALUES 
            ({", ".join(':' + name for name in columns)})
            """
            
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing bot data: {bindings}")
        cursor.execute(sql, bindings)
        connection.commit()
        connection.close()

    def get_bot_list(self):
        """
        returns a list of all bot ids stored in the database, including hidden ones
        """
        sql = """
        SELECT _id from bots
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute(sql).fetchall()
        conn.close()
        bot_ids = [row[0] for row in rows]
        
        return bot_ids
    
    def get_bot(self, bot_id:int)->Bot:
        sql = """
        SELECT * from bots WHERE _id = (:bot_id)
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
        bindings = {}
        for key, value in user_data.items():
            columns.append(key)
            bindings[key] = value
             
        sql = f"""
            INSERT OR REPLACE INTO 
            user
            ({", ".join(columns)})
            VALUES 
            ({", ".join(':' + name for name in columns)})
            """
            
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing user data: {bindings}")
        cursor.execute(sql, bindings)
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
        bindings = {}
        for key, value in message_data.items():
            columns.append(key)
            bindings[key] = value
             
        sql = f"""
            INSERT OR REPLACE INTO 
            messages
            ({", ".join(columns)})
            VALUES 
            ({", ".join(':' + name for name in columns)})
            """
            
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing message data: {bindings}")
        cursor.execute(sql, bindings)
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

    def get_conversation_list(self):
        """
        returns a list of all bot ids stored in the database, including hidden ones
        """
        sql = """
        SELECT _id from conversations
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute(sql).fetchall()
        conn.close()
        conversation_ids = [row[0] for row in rows]
        
        return conversation_ids
    
    def store_conversation(self, convo:Conversation)->None:
        """
        Note: this will store the messages and id of the bot that participated
        in the conversation, but it won't save the bot data itself
        """
        
        convo_data={}
        convo_data["_id"]=convo._id
        convo_data["title"]=convo.title
        convo_data["bot_id"] = convo.bot._id
        for position, msg in convo.messages.items():
            self.store_message(msg)
        
        
        columns = []
        bindings = {}
        for key, value in convo_data.items():
            columns.append(key)
            bindings[key] = value
             
        sql = f"""
            INSERT OR REPLACE INTO 
            conversations 
            ({", ".join(columns)})
            VALUES 
            ({", ".join(':' + name for name in columns)})
            """
            
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing conversation data: {bindings}")
        cursor.execute(sql, bindings)
        connection.commit()
        connection.close()
    
    def get_conversation(self,convo_id, bot_gallery:BotGallery)->Conversation:
        

        sql = """
            SELECT * FROM conversations WHERE _id = :_id        
        """
        bindings = {"_id":convo_id}
        connection = self.get_connection()
        cursor = connection.cursor()
        logger.info(f"Storing conversation data: {bindings}")
        rows = cursor.execute(sql, bindings).fetchall()
        column_names = [description[0] for description in cursor.description]
        convo_data = {name:value for name, value in zip(column_names,rows[0])}
        connection.commit()
        connection.close()

        messages = self.get_messages(conversation_id=convo_id)
        convo_id = convo_data["_id"]
        title = convo_data["title"]
        bot_id = convo_data["bot_id"]

        bot = bot_gallery.get_bot(bot_id)
        convo = Conversation(_id = convo_id, bot=bot, title=title, messages=messages)    
        return convo