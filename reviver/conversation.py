import openai
import reviver.log
from dataclasses import dataclass, field
from reviver.bot import Bot
from queue import Queue
from threading import Thread
import time
from reviver.gui.markdown_conversion import CONTENT_CSS
from PySide6.QtCore import QObject, Signal
from os import getenv
from reviver.message import Message

log = reviver.log.get(__name__)

class QtSignaler(QObject):
    """
    Not sure if this is necessary right now...but started building it out...
    """
    new_styled_message = Signal(Message) 
    new_styled_message = Signal(Message) 

@dataclass(frozen=False, slots=True)
class Conversation:
    _id: int
    bot: Bot 
    title: str = "untitled"
    messages: dict= field(default_factory=dict[int, Message])
    qt_signal:QtSignaler = QtSignaler()


    def __post_init__(self):
        prompt_message = Message(role = "system", content=self.bot.system_prompt)
        self.messages[0] = prompt_message
        
    def add_message(self, msg:Message)->None:
        self.messages[self.message_count+1] = msg
        self.qt_signal.new_styled_message.emit(msg)        

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
    
    def as_styled_html(self):
        
        # combine html into larger doc   
        joined_html = "<style>" + CONTENT_CSS + "</style>"      
        for position, msg in self.messages.items():
            joined_html += msg.as_styled_html()
        # styled_html = style_code_blocks(joined_html) 
        styled_html = joined_html
        return styled_html
        
        
    def generate_next_message(self, out_q:Queue=None):
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

            log.info(f"pinging server with message: {self.messages[self.message_count]}")
            
            # this ends up being a rather large block of code in the try...
            # I acknowledge that and I'm prepared to leave it for now...
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
            self.add_message(new_message)

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
                            self.qt_signal.new_styled_message.emit(new_message)

                    # the below is a quick-and-dirty solution to incorporate the weird output of gpt turbo instruct
                    if "text" in response.choices[0].keys():
                        new_word =response.choices[0]["text"]
                        reply += new_word
                        new_message.content = reply
                        time.sleep(.05)
                        self.qt_signal.new_styled_message.emit(new_message)

            new_message.content = reply 
            log.info(f"New reply is {reply}")
            self.qt_signal.new_styled_message.emit(new_message)

            # currently used primarily for testing...might be useful elsewhere
            if out_q is not None:
                out_q.put(new_message)

            if response_count == 0:
                log.info("No response")        

 
        thread = Thread(target=worker,args=[],daemon=True )
        thread.start()