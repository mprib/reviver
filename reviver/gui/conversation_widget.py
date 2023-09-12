import sys
from typing import Optional
from markdown import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from PySide6.QtWidgets import QTextEdit, QPushButton, QTextBrowser, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6 import Qt
from PySide6.QtCore import QTimer
import html
from reviver.conversation import Message, Conversation
from reviver.user import User
from reviver.bot import Bot
from datetime import datetime

import reviver.logger
log = reviver.logger.get(__name__)

CONTENT_CSS = """
<style>

/* General styles for all messages */
.message {
    font-family: Arial, sans-serif;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-left: 20px;
    padding-right: 20px;
    margin-bottom: 5px;
    border-radius: 5px;
}

/* User message styles */
.user {
    background-color: #95defb; 
    color: #000; /* Black */
    margin-right: 5%; /* Shift to left */
}

/* Bot message styles */
.assistant {
    background-color: #a8ffa4; 
    color: #000; /* Black */
    margin-left: 5%; /* Shift to right */
}

/* System message styles */
.system {
    background-color: #dcdcdc; /* Gray*/
    color: #000; /* Black */
    font-style: italic;
}

.bot_name {
    font-family: monospace;
    font-style: bold;
    margin-left: 5%; /* Shift to right */
  
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

class ConversationWidget(QWidget):
    def __init__(self, conversation:Conversation):
        super().__init__()
        self.conversation = conversation

        self.chat_display = QWebEngineView()
        self._chat_display = QWebEngineView()
        self.text_entry = QTextEdit()
        self.send_text = QPushButton("&send")

        self.place_widgets()
        self.connect_widgets()
        self.chat_display.setHtml(self.conversation.as_styled_html())
        
             
    def place_widgets(self):
        
        self.setLayout(QVBoxLayout())
        
        self.layout().addWidget(self.chat_display)
        self.layout().addWidget(self.text_entry)
        self.layout().addWidget(self.send_text)
        
    def connect_widgets(self):
        self.send_text.clicked.connect(self.send_message) 
        self.chat_display.loadFinished.connect(self.scroll_to_bottom)
    
    def send_message(self):
        log.info(f"Sending: {self.text_entry.toPlainText()}")
        new_message  = Message(self.conversation._id, role= "user", content=self.text_entry.toPlainText())
        self.conversation.add_message(new_message)
    
        # Add a new message to the end of the conversation
        js_code = f'''
        var element = document.createElement('div');
        element.innerHTML = `{new_message.as_html()}`;
        document.body.appendChild(element);
        window.scrollTo(0, document.body.scrollHeight);
        '''
        self.chat_display.page().runJavaScript(js_code)

        log.info(f"Current location is {self.chat_display.page().scrollPosition()}") 

    # def send_message(self):
    #     log.info(f"Sending: {self.text_entry.toPlainText()}")
    #     new_message  = Message(self.conversation._id, role= "user", content=self.text_entry.toPlainText())
    #     self.conversation.add_message(new_message)
    #     self.chat_display.setHtml(self.conversation.as_styled_html())
    #     log.info(f"Current location is {self.chat_display.page().scrollPosition()}")

    #     # Schedule the scroll operation
    #     # QTimer.singleShot(7, self.scroll_to_bottom)        

    def scroll_to_bottom(self):
        # Scroll the off-screen display to the bottom
        log.info("_chat_display load finished")
        self.chat_display.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);")
    
        
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

    convo_widget = ConversationWidget(convo)

    convo_widget.show()
    app.exec()   
