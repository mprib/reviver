
import reviver.logger
logger = reviver.logger.get(__name__)
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str
    time: datetime = datetime.now()

    @property
    def token_size(self):
        """
        Token size is a generalization based on the rule that 1 token ~= 4 characters:
        https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        """
        return len(self.content)/4

    @property
    def chat_bubble(self):
       return {"role":self.role, "content":self.content} 
 
@dataclass(frozen=False, slots=True)
class Conversation:
    messages: list = field(default_factory=list[Message])

    def add_message(self, msg:Message)->None:
        self.messages.append(msg)
        
    def to_string_list(self):
        
        msgs_for_load = [] 
        for msg in self.messages:
            msgs_for_load.append(msg.chat_bubble)
        return msgs_for_load

    @property
    def token_size(self):
        size = 0
        for msg in self.messages:
            size+=msg.token_size
        return size