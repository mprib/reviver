import rtoml
import reviver.logger
from dataclasses import dataclass, asdict
logger = reviver.logger.get(__name__)
from pathlib import Path
from reviver.conversation import Conversation, Message
from reviver.bot import Bot

class Archiver:
    
    def __init__(self, user_profile_dir:Path) -> None:
        self.profile_dir = user_profile_dir

    def store_conversation(self, convo:Conversation) -> None:
        toml_data = {}
        toml_data["bot"] = asdict(convo.bot)

        messages = get_messages_for_toml(convo)     
        toml_data["messages"] = messages
        logger.info(messages)        

        # conversations are stored under bot subfolder
        
        target_dir = Path(self.profile_dir, convo.bot.name)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = Path(target_dir, f"{convo.title}.toml")

        with open(target_path, "w") as f:
            rtoml.dump(toml_data,f)


    def get_bot(self, bot_name:str, title:str)->Bot:
        target_dir = Path(self.profile_dir, bot_name)
        target_path = Path(target_dir, f"{title}.toml")

        conversation_data = rtoml.load(target_path)
        bot_data = conversation_data["bot"]
        bot = Bot(**bot_data)
        
        return bot
        
    def get_messages_from_toml(self, bot:Bot, title:str)->dict[int:Message]:
        target_dir = Path(self.profile_dir, bot.name)
        target_path = Path(target_dir, f"{title}.toml")

        toml_data = rtoml.load(target_path)
        messages = {}
        for msg in toml_data["messages"]:
            role = msg["role"]
            content = msg["content"]
            time = msg["time"]
            index = msg["index"]

            messages[index] = Message(role, content,time)

        logger.info(f"Messages loaded")
        return messages

    def get_conversation(self, bot:Bot, title:str) -> Conversation:
        
        messages = self.get_messages_from_toml(bot,title) 
        message_count = len(messages.keys())
        convo = Conversation(bot, messages,message_count)
        return convo
    


def get_messages_for_toml(convo:Conversation):
    messages = []
    logger.info(convo.messages_prompt)
    for index,msg in convo.messages.items():
        msg_data = asdict(msg)
        msg_data["index"] = index
        messages.append(msg_data)
    
    return messages 

   