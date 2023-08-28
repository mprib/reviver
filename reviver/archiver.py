import rtoml
import reviver.logger
from dataclasses import dataclass
logger = reviver.logger.get(__name__)
from pathlib import Path
from reviver.conversation import Conversation

class Archiver:
    
    def __init__(self, chat_history_dir:Path) -> None:
        self.chat_history_dir = chat_history_dir

        pass


    def store_conversation(convo:Conversation):
        pass


