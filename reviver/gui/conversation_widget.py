from PySide6.QtWidgets import QTextEdit, QPushButton, QTextBrowser, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtWebEngineWidgets import QWebEngineView
from reviver.conversation import Message, Conversation
from reviver.user import User
from reviver.bot import Bot
from pathlib import Path
from reviver import ROOT
import json
import reviver.log
log = reviver.log.get(__name__)

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
        new_message  = Message(role= "user", content=self.text_entry.toPlainText())
        self.text_entry.clear() # no longer needed now that message is created
        self.conversation.add_message(new_message)
        self.conversation.generate_next_message()

        
    def add_styled_message_to_webview(self, msg:Message):
        # Add a new message to the end of the conversation
        # styled_html = msg.backtic_complete_content
        # styled_html = json.dumps(styled_html)
        styled_html = msg.as_styled_html()
        js_code = f'''
        var element = document.getElementById('{msg._id}');
        if (element) {{
            element.innerHTML = `{styled_html}`;
        }} else {{
            var newElement = document.createElement('div');
            newElement.id = '{msg._id}';
            newElement.innerHTML = `{styled_html}`;
            document.body.appendChild(newElement);
        }}
        window.scrollTo(0, document.body.scrollHeight);
        '''
        self.chat_display.page().runJavaScript(js_code)

        
if __name__=="__main__":
    
    import dotenv
    key_location=Path(ROOT, ".env")
    dotenv.load_dotenv(key_location)

    app = QApplication([])

    user = User(name="Me The User", dot_env_loc=key_location)

    log.info(user.keys)
    # return f'{CONTENT_CSS}<style>{code_css}</style>' + str(soup)
    model = "jondurbin/airoboros-l2-70b-2.1"
    model = "meta-llama/codellama-34b-instruct"
    model = "gryphe/mythomax-l2-13b"
    model = "openai/gpt-4"
    model = "openai/gpt-3.5-turbo-0301"
    bot = Bot(_id=1,name="rocket_logic", model=model, rank=1, max_tokens=5000)
    convo = Conversation(_id = 1, bot=bot)

    convo_widget = ConversationWidget(convo)

    convo_widget.show()
    app.exec()   
