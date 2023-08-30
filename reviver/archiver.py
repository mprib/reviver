import rtoml
import reviver.logger
from dataclasses import dataclass, asdict
logger = reviver.logger.get(__name__)
from pathlib import Path
from reviver.conversation import Conversation
from reviver.bot import Bot

class Archiver:
    
    def __init__(self, user_profile_dir:Path) -> None:
        self.profile_dir = user_profile_dir

    def store_conversation(self, convo:Conversation):
        toml_data = {}
        toml_data["bot"] = asdict(convo.bot)

        messages = get_messages_for_toml_table(convo)     
        toml_data["messages"] = messages
        logger.info(messages)        

        # conversations are stored under bot subfolder
        
        target_dir = Path(self.profile_dir, convo.bot.name)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = Path(target_dir, f"{convo.title}.toml")

        with open(target_path, "w") as f:
            rtoml.dump(toml_data,f)



def get_messages_for_toml_table(convo:Conversation):
    messages = []
    logger.info(convo.messages_prompt)
    for index,msg in convo.messages.items():
        msg_data = asdict(msg)
        msg_data["index"] = index
        messages.append(msg_data)
    
    return messages 

   