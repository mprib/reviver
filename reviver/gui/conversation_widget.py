from PySide6.QtWidgets import QTextEdit, QPushButton, QTextBrowser, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtWebEngineWidgets import QWebEngineView
from reviver.conversation import Message, Conversation
from reviver.user import User
from reviver.bot import Bot
from pathlib import Path
from reviver import ROOT
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
        self.send_text.clicked.connect(self.create_user_message) 
        self.conversation.qt_signal.new_styled_message.connect(self.add_styled_message_to_webview)

        
    def create_user_message(self):
        log.info(f"Sending: {self.text_entry.toPlainText()}")
        # self.text_entry.setEnabled(False)
        new_message  = Message(self.conversation._id, role= "user", content=self.text_entry.toPlainText())
        self.text_entry.clear() # no longer needed now that message is created
        self.conversation.add_message(new_message)
        self.conversation.generate_next_message()

        
    def add_styled_message_to_webview(self, msg:Message):
        # Add a new message to the end of the conversation
        js_code = f'''
        var element = document.getElementById('{msg._id}');
        if (element) {{
            element.innerHTML = `{msg.as_styled_html()}`;
        }} else {{
            var newElement = document.createElement('div');
            newElement.id = '{msg._id}';
            newElement.innerHTML = `{msg.as_styled_html()}`;
            document.body.appendChild(newElement);
        }}
        window.scrollTo(0, document.body.scrollHeight);
        '''
        self.chat_display.page().runJavaScript(js_code)

        
if __name__=="__main__":
    
    app = QApplication([])

    key_location=Path(ROOT, "keys.toml")
    user = User(name="Me The User", key_location=key_location)

    log.info(user.keys)
    model = "jondurbin/airoboros-l2-70b-2.1"
    bot = Bot(_id=1,name="rocket_logic", model=model, rank=1, max_tokens=2000)
    convo = Conversation(_id = 1, user=user, bot=bot)

    convo_widget = ConversationWidget(convo)

    convo_widget.show()
    app.exec()   
