import reviver.log
from dataclasses import asdict
from pathlib import Path
from reviver.conversation import Conversation, Message
from reviver.bot import Bot, BotGallery
import rtoml


log = reviver.log.get(__name__)


class Archive:
    """
    Aims for simplicity in implementation/auditing/tweaking by storing all data in toml files
    """
    def __init__(self, reviver_data_dir: Path) -> None:
        self.reviver_dir = reviver_data_dir
        self.bots_dir = Path(self.reviver_dir, "bots")
        self.conversations_dir = Path(self.reviver_dir, "conversations")

        # check that appropriate directories exist
        self.bots_dir.mkdir(parents=True, exist_ok=True)
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        
    def bot_path(self, bot_name:str)->Path:
        return Path(self.bots_dir, str(bot_name)+".toml")
     
    def store_bot(self, bot: Bot) -> None:
        bot_data = asdict(bot)
        log.info(f"Storing... {bot.name}")
        with open(self.bot_path(bot.name), "w+") as f:
            rtoml.dump(bot_data,f)    


    def store_bot_gallery(self, bot_gallery:BotGallery):
        for bot_id, bot in bot_gallery.bots.items():
            self.store_bot(bot)
            
    
        
    def load_bot_gallery(self):
        bots = {}
        for bot_toml in Path(self.reviver_dir, "bots").iterdir():
            bot_name = bot_toml.stem
            bot = self.get_bot(bot_name)
            bots[bot_name] = bot
        
        bot_gallery = BotGallery(bots)
        return bot_gallery
         
        
    def get_bot(self, bot_name:str) -> Bot:
        bot_data = rtoml.load(self.bot_path(bot_name))
        bot = Bot(**bot_data)
        return bot


    def get_messages(self, conversation_id: int) -> dict[int, Message]:
        # need to get all message positions first
        sql = """
        SELECT position FROM messages WHERE conversation_id = :conversation_id
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        rows = cursor.execute(sql, {"conversation_id": conversation_id}).fetchall()

        msg_positions = [position[0] for position in rows]

        log.info(f"Message positions are:{msg_positions}")

        messages = {
            position: self.get_message(conversation_id, position)
            for position in msg_positions
        }

        return messages

    def store_message(self, message: Message) -> None:
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
        log.info(f"Storing message data: {bindings}")
        cursor.execute(sql, bindings)
        connection.commit()
        connection.close()

    def get_message(self, conversation_id: int, position: int) -> Message:
        sql = """
        SELECT * FROM messages WHERE conversation_id=? AND position =?
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        rows = cursor.execute(sql, (conversation_id, position)).fetchall()
        column_names = [description[0] for description in cursor.description]
        msg_data = {name: value for name, value in zip(column_names, rows[0])}
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

    def store_conversation(self, convo: Conversation) -> None:
        """
        Note: this will store the messages and id of the bot that participated
        in the conversation, but it won't save the bot data itself
        """

        convo_data = {}
        convo_data["_id"] = convo._id
        convo_data["title"] = convo.title
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
        log.info(f"Storing conversation data: {bindings}")
        cursor.execute(sql, bindings)
        connection.commit()
        connection.close()

    def get_conversation(
        self, convo_id, bot_gallery: BotGallery
    ) -> Conversation:
        sql = """
            SELECT * FROM conversations WHERE _id = :_id        
        """
        bindings = {"_id": convo_id}
        connection = self.get_connection()
        cursor = connection.cursor()
        log.info(f"Storing conversation data: {bindings}")
        rows = cursor.execute(sql, bindings).fetchall()
        column_names = [description[0] for description in cursor.description]
        convo_data = {name: value for name, value in zip(column_names, rows[0])}
        connection.commit()
        connection.close()

        messages = self.get_messages(conversation_id=convo_id)
        convo_id = convo_data["_id"]
        title = convo_data["title"]
        bot_id = convo_data["bot_id"]

        bot = bot_gallery.get_bot(bot_id)
        convo = Conversation(
            _id=convo_id, bot=bot, title=title, messages=messages
        )
        return convo
