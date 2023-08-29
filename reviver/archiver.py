import rtoml
import reviver.logger
from dataclasses import dataclass, asdict
logger = reviver.logger.get(__name__)
from pathlib import Path
from reviver.conversation import Conversation


class Archiver:
    
    def __init__(self, chat_history_dir:Path) -> None:
        self.chat_history_dir = chat_history_dir

    def store_conversation(self, convo:Conversation):
        
        messages = []
        logger.info(convo.prompt)
        for index,msg in convo.messages.items():
            msg_data = asdict(msg)
            msg_data["index"] = index
            messages.append(msg_data)
            
        logger.info(messages)        

        messages_for_toml_table = {"messages":messages}

        target_path = Path(self.chat_history_dir, f"{convo.title}.toml")
        with open(target_path, "w") as f:
            rtoml.dump(messages_for_toml_table,f)
