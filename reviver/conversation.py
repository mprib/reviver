
import reviver.logger
logger = reviver.logger.get(__name__)
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str
    time: datetime

    @property
    def token_size(self):
        """
        Token size is a generalization based on the rule that 1 token ~= 4 characters:
        https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        """
        len(self.content)/4
        
    @property
    def chat_bubble(self):
       return {"role":self.role, "content":self.content} 
 
@dataclass(frozen=False, slots=True)
class Conversation:
    messages: list[Message]