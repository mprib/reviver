import reviver.log
from dataclasses import dataclass
from datetime import datetime
from reviver.gui.markdown_conversion import style_code_blocks
import markdown

log = reviver.log.get(__name__)

@dataclass(slots=True, frozen=False) # not frozen because content of message is built up iteratively
class Message:
    """
    The bulk of this class is dedicated to processing the core data to be formatted appropriately in the webview widget
    """
    role: str
    content: str
    time: str = None

    def __post_init__(self):
        self.time = datetime.now()
        
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
        _id = f"message-{self.time}"
        return _id
        
    @property
    def token_size(self):
        """
        Token size is a generalization based on the rule that 1 token ~= 4 characters:
        https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        """
        return len(self.content)/4

    # @property
    # def chat_bubble(self):
    #    return {"role":self.role, "content":self.content} 

    @property
    def time_as_datetime(self):
        format = "%Y-%m-%d %H:%M:%S.%f"
        t = datetime.strptime(self.time, format)
        return t

    def as_html(self):
        # html_version = markdown.markdown(self.content, extensions=['fenced_code'])
        html_version = markdown.markdown(self.backtic_complete_content, extensions=['fenced_code'])
        return html_version
        
    def as_styled_html(self):
        styled_html=""
        if self.role == "assistant":
            styled_html+= "<div class='bot_name' <p> bot </p></div>"
        
        styled_html += f"""<div id='{self._id}' class='message {self.role}'>
                            {"<p>SYSTEM PROMPT</p>" if self.role == "system" else ""}
                            {self.as_html()}
                        </div>
                        """
        styled_html = style_code_blocks(styled_html)

        return styled_html
