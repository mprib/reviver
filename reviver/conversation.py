import openai
import reviver.logger
from dataclasses import dataclass, field
from datetime import datetime
from reviver.bot import Bot
from reviver.user import User
from queue import Queue
from threading import Thread
import sys
from reviver.gui.markdown_conversion import style_code_blocks, CONTENT_CSS
import markdown
from PySide6.QtCore import QObject, Signal


log = reviver.logger.get(__name__)

@dataclass
class Message:
    conversation_id:int
    role: str
    content: str
    position:int = None
    time: str = str(datetime.now())

    @property
    def backtic_complete_content(self) -> str:
        """
        Used to make sure that the stylized html will render python correctly when it is in the middle
        of being drafted by the bot.
        """
        # check if the content has an odd number of triple backticks
        if self.content.count('```') % 2 != 0:
            # if so, append a set of triple backticks to the end
            return self.content + '\n```'
        else:
            return self.content

    @property
    def _id(self):
        """
        Used to identify specific message divisions in conversation widget's webview html 
        """
        return f"message-{self.conversation_id}-{self.position}"
        
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

    @property
    def time_as_datetime(self):
        format = f"%Y-%m-%d %H:%M:%S.%f"
        t = datetime.strptime(self.time, format)
        return t

    def as_html(self):
        # html_version = markdown.markdown(self.content, extensions=['fenced_code'])
        html_version = markdown.markdown(self.backtic_complete_content, extensions=['fenced_code'])
        return html_version
        
    def as_styled_html(self):
        styled_html=""
        if self.role == "assistant":
            styled_html+= f"<div class='bot_name' <p> bot </p></div>"
        
        styled_html += f"""<div id='{self._id}' class='message {self.role}'>
                            {"<p>SYSTEM PROMPT</p>" if self.role == "system" else ""}
                            {self.as_html()}
                        </div>
                        """
        styled_html = style_code_blocks(styled_html)

        return styled_html

class QtSignaler(QObject):
    """
    Not sure if this is necessary right now...but started building it out...
    """
    new_styled_message = Signal(Message) 
    new_styled_message = Signal(Message) 

@dataclass(frozen=False, slots=True)
class Conversation:
    _id: int
    user: User
    bot: Bot 
    title: str = "untitled"
    messages: dict= field(default_factory=dict[int, Message])
    qt_signal:QtSignaler = QtSignaler()

    def get_writer_name(self, role:str)->str:
        match role:
            case "user":
                return self.user.name
            case "assistant":
                return self.bot.name
            case "system":
                return "system"

    def __post_init__(self):
        prompt_message = Message(conversation_id=self._id,
                                 position=0,
                                 role = "system",
                                 content=self.bot.system_prompt
                                 )
        self.messages[0] = prompt_message
        
    def add_message(self, msg:Message)->None:
        next_position = self.message_count+1
        msg.position = next_position
        self.messages[next_position] = msg
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

        msgs_for_load = [] 
        for index, msg in self.messages.items():
            msgs_for_load.append(msg.chat_bubble)
        return msgs_for_load

    @property
    def token_size(self):
        size = 0
        for index, msg in self.messages.items():
            size+=msg.token_size
        return size
    
    def as_styled_html(self):
        
        # combine html into larger doc   
        joined_html = CONTENT_CSS        
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
            openai.api_key = self.user.keys["OPEN_ROUTER_API_KEY"]

            # Set the headers to identify your app
            headers = {
                "HTTP-Referer": "https://github.com/mprib/reviver",  # Replace with your actual site URL
                "X-Title": "Festival Cobra",  # Replace with your actual app name
            }

            log.info(f"pinging server with message: {self.messages[self.message_count]}")
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
            new_message = Message(conversation_id=self._id, role="assistant", content="")
            self.add_message(new_message)

            reply = ""
            response_count = 0
            for response in response_stream:
                response_count +=1  
                if hasattr(response, "choices"):
                    delta = response.choices[0]["delta"]
                    if delta != {}:
                        new_word = delta["content"]
                        reply += new_word
                        new_message.content = reply
                        self.qt_signal.new_styled_message.emit(new_message)
                        # self.qt_signal.new_plain_message.emit(new_message)

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