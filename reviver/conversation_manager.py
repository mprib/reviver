
import openai
import reviver.log
from dataclasses import dataclass, field
from reviver.bot import Bot
from queue import Queue
from threading import Thread
import time
from PySide6.QtCore import QObject, Signal
from os import getenv
from datetime import datetime
from reviver.message import Message
from reviver.conversation import Conversation
import reviver.log
log = reviver.log.get(__name__)

@dataclass(frozen=False, slots=True)
class ConversationManager:
    """
    Provides a central interface for all conversations and maintains a pointer
    to an active conversation
    """

    conversations: dict = field(default_factory=dict[str,Conversation])
    active_conversation:Conversation = None    
    
    def _add_conversation(self, convo:Conversation)->None:
        self.conversations[convo.title] = convo
    
    def remove_conversation(self, convo_title)->None:
        self.conversations[convo_title].pop()

    def rename_conversation(self, old_title, new_title)->None:
        convo = self.conversations.pop(old_title)
        convo.title = new_title
        self.conversations[new_title] = convo
        
        
    def get_conversation_list(self)->list:
        """
        returns a list of all conversations sorted in descending
        order by the last time that a message was sent 
        """
        
        sorted_conversations = sorted(list(self.conversations.values()), key = lambda conversation:conversation.last_update)
        reversed_conversations = reversed(sorted_conversations) # want descending with most recent first
        conversation_titles = [convo.title for convo in reversed_conversations]

        return conversation_titles
    
    def new_active_conversation(self,bot:Bot):
        """
        When starting a conversation it will always become the 
        active conversation
        """

        convo_title = str(datetime.now())
        for char in [":", " ", ".", "-"]:
            convo_title = convo_title.replace(char, "")

        convo = Conversation(bot=bot, title=convo_title)
        self.conversations[convo_title] = convo
        self.active_conversation = convo
    

    def set_active_conversation(self, convo_title):
        self.active_conversation = self.conversations[convo_title]