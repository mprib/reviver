import openai
import reviver.log
from dataclasses import dataclass
from reviver.bot import Bot
from queue import Queue
from threading import Thread
import time
from PySide6.QtCore import QObject, Signal
from os import getenv
from reviver.message import Message

log = reviver.log.get(__name__)

@dataclass(frozen=False, slots=True)
class Conversation:
    bot: Bot 
    title: str = "untitled"
    messages: dict = None


    def __post_init__(self):
        if self.messages is None:
            self.messages = {}
            #only create a new prompt message if you aren't loading in from the archive...
            prompt_message = Message(role = "system", content=self.bot.system_prompt)
            self.messages[0] = prompt_message
        
    def _add_message(self, msg:Message)->None:
        self.messages[self.message_count] = msg
    
    def add_user_message(self, content:str, message_added:Signal=None):
        new_message =Message(role="user", content=content)
        self._add_message(new_message)
        if message_added is not None:
            log.info(f"Signalling the new message has been added...")
            message_added.emit(new_message._id,new_message.role, new_message.content)


    @property
    def message_count(self):
        count = len(self.messages.keys())
        return count


    @property
    def messages_prompt(self):
        """
        This will return the conversation data in the format that is expected by the model
        """

        message_history = [] 
        for index, msg in self.messages.items():
            role_content = {"role":msg.role, "content":msg.content}
            message_history.append(role_content)
        return message_history

    @property
    def token_size(self):
        size = 0
        for index, msg in self.messages.items():
            size+=msg.token_size
        return size
    
        
        
    def generate_reply(self, out_q:Queue=None, message_added:Signal=None, message_updated:Signal=None, message_complete:Signal=None):
        """
        call to API and get next message
        message is added to self.messages
        if out_q is provided, then message is passed along on it in addition to being added
        """

        def worker():
            # Set the base API URL and your OpenRouter API key
            openai.api_base = "https://openrouter.ai/api/v1"
            openai.api_key = getenv("OPEN_ROUTER_API_KEY")

            # Set the headers to identify your app
            headers = {
                "HTTP-Referer": "https://github.com/mprib/reviver",  # Replace with your actual site URL
                "X-Title": "Festival Cobra",  # Replace with your actual app name
            }

            log.info(f"pinging server with message: {self.messages[self.message_count-1]}")
            
            response_stream = openai.ChatCompletion.create(
                    model=self.bot.model, 
                    messages=self.messages_prompt,
                    headers=headers,
                    temperature = self.bot.temperature,
                    max_tokens = self.bot.max_tokens,
                    top_p=self.bot.top_p,
                    frequency_penalty=self.bot.frequency_penalty,
                    presence_penalty=self.bot.presence_penalty,
                    stream=True
                )

            # create a new empty message
            new_message = Message(role="assistant", content="")
            self._add_message(new_message)
            if message_added is not None:
                message_added.emit(new_message._id,new_message.role, new_message.content)

            reply = ""
            response_count = 0
            for response in response_stream:
                response_count +=1  
                if hasattr(response, "choices"):
                    if "delta" in response.choices[0].keys():
                        delta = response.choices[0]["delta"]
                        if delta != {}:
                            new_word = response.choices[0]["delta"]["content"]
                            reply += new_word
                            new_message.content = reply
                            time.sleep(.05)
                            if message_updated is not None:
                                message_updated.emit(new_message._id, new_message.role, new_message.content)

                    # below is a quick-and-dirty solution to incorporate the weird output of gpt turbo instruct
                    if "text" in response.choices[0].keys():
                        new_word =response.choices[0]["text"]
                        reply += new_word
                        new_message.content = reply
                        time.sleep(.05)
                        if message_updated is not None:
                            message_updated.emit(new_message._id, new_message.role, new_message.content)

            new_message.content = reply 
            log.info(f"New reply is {reply}")
            if message_complete is not None:
                message_complete.emit()

            # currently used primarily for testing...might be useful elsewhere
            if out_q is not None:
                out_q.put(new_message)

            if response_count == 0:
                log.info("No response")        

        thread = Thread(target=worker,args=[],daemon=True )
        thread.start()


    def __eq__(self, other):
        """
        needed to validate test assertion...and debug archive issues.
        """
        if isinstance(other, Conversation):
            bots_equal = self.bot == other.bot
            log.info(f"Bots equal?:{bots_equal}")
            titles_equal = self.title == other.title
            log.info(f"titles equal?:{titles_equal}")
            messages_equal = self.messages == other.messages
            log.info(f"Messages equal?:{messages_equal}")
            equality = bots_equal and titles_equal and messages_equal
            log.info(f"Equal?:{equality}")
            return equality
        return False
    
    
