
import reviver.logger
logger = reviver.logger.get(__name__)
from dataclasses import dataclass, field
from datetime import datetime
from reviver.bot import Bot

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
    bot: Bot 
    messages: dict= field(default_factory=dict[int, Message])
    message_count: int = 0

    def add_message(self, msg:Message)->None:
        self.messages[self.message_count] = msg
        self.message_count += 1

    @property
    def messages_prompt(self):
        """
        This will return the conversation data in the format that is expected by the model
        """
        msgs_for_load = [] 
        for index, msg in self.messages.items():
            msgs_for_load.append(msg.chat_bubble)
        return msgs_for_load
        
    @property
    def title(self):
        # need to sort this out in a bit...I think there is a way to pull it
        return "testing"
    
     
    @property
    def token_size(self):
        size = 0
        for index, msg in self.messages.items():
            size+=msg.token_size
        return size