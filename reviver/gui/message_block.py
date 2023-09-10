import sys
from typing import Optional
from markdown import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6 import Qt
import html
from reviver.conversation import Message, Conversation
from reviver.user import User
from reviver.bot import Bot
from datetime import datetime

import reviver.logger
log = reviver.logger.get(__name__)

CONTENT_CSS = """
<style>
body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f8f8;
  padding: 1em;
}

h1 {
  font-size: 1.5em; 
  color: #444;
}

h2, h3, h4, h5, h6 {
  color: #444;
}

a {
  color: #0645ad;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code, pre {
  font-family: 'ui-monospace', 'Cascadia Mono', 'Segoe UI Mono', 'Liberation Mono', Menlo, Monaco, Consolas, monospace;
  border-radius: 3px;
  padding: 0.2em 0.4em;
}

pre {
  padding: 1em;
  overflow: auto;
}

pre code {
  background: none;
  border: none;
  padding: 0
</style>
"""

class ConversationDisplay(QWidget):
    def __init__(self, conversation:Conversation):
        super().__init__()
        self.conversation = conversation

        self.place_message_blocks()

    
    def place_message_blocks(self):
        self.setLayout(QVBoxLayout())

        for position, message in self.conversation.messages.items():
            
            match message.role:
                case "user":
                    writer_name = self.conversation.user.name
                case "assistant":
                    writer_name = self.conversation.bot.name
                case "system":
                    writer_name = "system"
                    
            new_message = MessageBlock(message, writer_name)
            self.layout().addWidget(new_message)

class MessageBlock(QWidget):
    
    def __init__(self, message:Message, writer_name:str):
        super().__init__()
        self.message = message

        self.content_block = ContentBlock(self.message.content)

        self.writer_name = writer_name
        
        self.writer_label = QLabel()
        self.writer_label.setText(f"<b>{self.writer_name}<\b>")

        self.time_label = QLabel()
        self.time_label.setText(self.message.time)
        
        # get time
        self.time = self.message.time 
        
        self.place_widgets() 

    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        self.banner = QHBoxLayout()
        self.banner.addWidget(self.writer_label)
        # self.banner.addWidget(self.time_label)
        self.layout().addLayout(self.banner)
        self.layout().addWidget(self.content_block)

class ContentBlock(QWebEngineView):
    def __init__(self, content:str):
        super().__init__()
        self.content = content        
        plain_html = convert_markdown_to_html(self.content) 
        self.html = style_code_blocks(plain_html)
        self.setHtml(self.html) 
    
        # Run JavaScript to get the height once the page is fully loaded
        self.loadFinished.connect(self.adjust_height)

    def adjust_height(self):
        self.page().runJavaScript("document.documentElement.scrollHeight",0, self.set_height)

    def set_height(self, height):
        log.info(f"Setting fixed height to {height}")
        self.setFixedHeight(height)

        
def convert_markdown_to_html(input_text):
    html_version = markdown(input_text, extensions=['fenced_code'])
    return html_version

def style_code_blocks(html):
    soup = BeautifulSoup(html, 'html.parser')

    formatter = HtmlFormatter(style='monokai', full=False, cssstyles='overflow:auto;')

    code_css = formatter.get_style_defs('.highlight')

    for block in soup.find_all('code'):
        language = block.get('class', [None])[0]
        if language is not None:
            language = language[9:]  # remove 'language-' prefix
        code = block.string

        if language is None:
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(language)

        highlighted_code = highlight(code, lexer, formatter)
        block.string.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))
        log.info("not really sure what's going on here...")
    # Add the CSS to the beginning of the HTML string
    return f'{CONTENT_CSS}<style>{code_css}</style>' + str(soup)


    

if __name__=="__main__":
    


    content = """
    
This is some basic content. Lets
just keep this here
    
for now. 
    
```python
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")

# comment
def display_html_in_qwebengineview(html_content):
    app = QApplication([])
    view = QWebEngineView()
    unescaped_html = html.unescape(html_content)
    view.setHtml(unescaped_html)
    view.show()
    sys.exit(app.exec())
```

#why do I even care?
    
The story of stuff and things. 

This is something that I'm going to *emphasize*. I don't really know what to do about that.

Oh and here's a link [googl](www.google.com)

- this is a point
- here is anotehr one

- and again  
"""
    app = QApplication([])

    user = User(name="Me The User")
    bot = Bot(_id=1,name="friend", model="random", rank=1)
    convo = Conversation(_id = 1, user=user, bot=bot)
    msg1 = Message(1, "user", content=content,position=1)
    msg2 = Message(2, "assistant", content=" This is some *stuff*",position=2)

    convo.add_message(msg1)
    convo.add_message(msg2)
    convo_display = ConversationDisplay(convo)

    # convo_display.show()
    scroll = QScrollArea()
    scroll.setWidget(convo_display)
    scroll.show()

    # log.info(msg1.time_as_datetime)
    # full_block = MessageBlock(msg1, user.name)
    # full_block.show()
    # block = ContentBlock(msg.content)
    # block.show()
    
    sys.exit(app.exec())