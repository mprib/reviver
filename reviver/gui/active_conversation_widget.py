from typing import Optional
from PySide6.QtWidgets import (
    QTextEdit,
    QPushButton,
    QApplication,
    QComboBox,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from PySide6.QtWebEngineWidgets import QWebEngineView

# from reviver.conversation import Message, Conversation
# from reviver.bot import Bot
from reviver.controller import Controller
from pathlib import Path
from reviver import ROOT
from reviver.gui.html_styler import style_message
from reviver.gui.bot_manager_widget import BotGalleryWidget
import reviver.log

log = reviver.log.get(__name__)


class ActiveBotComboBox(QComboBox):
    def __init__(self, controller:Controller):
        super().__init__()
        self.controller = controller
        self.connect_widgets()
        self.update()

    def connect_widgets(self):
        self.currentTextChanged.connect(self.controller.set_active_convo_bot)
        self.controller.bot_added.connect(self.update)     
        self.controller.bots_reordered.connect(self.update)
        self.controller.bot_renamed.connect(self.update)

    def update(self):
        log.info(f"Updating bot combo box...")
        self.clear()
        for bot_name in self.controller.get_ranked_bot_names():
            self.addItem(bot_name)
    
            

class ActiveConversationWidget(QWidget):
    """
    A window to the active conversation in the controller layer
    """

    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.bot_select = ActiveBotComboBox(self.controller)
        self.bot_edit_btn = QPushButton(f"Bot")
        self.chat_display = QWebEngineView()
        self.text_entry = QTextEdit()
        self.send_text = QPushButton("&send")

        self.place_widgets()
        self.connect_widgets()
        self.display_active_conversation()

    def display_active_conversation(self):
        log.info(f"Active bot name being set to {self.controller.get_active_bot_name()}")
        self.bot_select.setCurrentText(self.controller.get_active_bot_name())
        self.chat_display.setHtml(self.controller.get_active_conversation_html())

    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        
        self.bot_header = QHBoxLayout()
        self.bot_header.addWidget(self.bot_select) 
        self.bot_header.addWidget(self.bot_edit_btn)

        self.layout().addLayout(self.bot_header)
        self.layout().addWidget(self.chat_display)
        self.layout().addWidget(self.text_entry)
        self.layout().addWidget(self.send_text)

    def connect_widgets(self):
        self.send_text.clicked.connect(self.send_user_message)
        self.bot_edit_btn.clicked.connect(self.launch_bot_manager)
        # self.controller.message_complete.connect(self.add_message)
        self.controller.message_added.connect(self.add_message)
        self.controller.message_updated.connect(self.update_message)
        self.controller.refresh_active_conversation.connect(self.display_active_conversation)
        self.controller.new_active_conversation.connect(self.display_active_conversation)
        self.controller.bot_updated.connect(self.display_active_conversation)
    
    def launch_bot_manager(self):
        self.bot_manager = BotGalleryWidget(self.controller)
        self.bot_manager.show()
         
    def send_user_message(self):
        log.info(f"Sending: {self.text_entry.toPlainText()}")
        # self.text_entry.setEnabled(False)
        # new_message = Message(role="user", content=self.text_entry.toPlainText())
        content = self.text_entry.toPlainText()
        log.info(f"Plain text being sent is {content}")
        self.controller.add_new_user_message(content)
        self.text_entry.clear()  # no longer needed now that message is created

    def add_message(self, msg_id: str, role: str, content: str = None):
        # Add a new message to the end of the conversation

        if content is None:
            styled_content = "..."
        else:
            styled_content = style_message(msg_id, role, content)
        log.info(f"Adding new message <div> with id: {msg_id}")
        js_code = f"""
        var newElement = document.createElement('div');
        newElement.id = '{msg_id}';
        newElement.innerHTML = `{styled_content}`;
        document.body.appendChild(newElement);
        window.scrollTo(0, document.body.scrollHeight);
        """
        self.chat_display.page().runJavaScript(js_code)

    def update_message(self, msg_id: str, role: str, content: str):
        # if the message has already been added (i.e. it is in progress)
        # just update the html with the message's styled html
        # log.info(f"Updating message <div> with id: {msg_id}; html: {styled_html}")
        if content is None:
            styled_content = "..."
        else:
            styled_content = style_message(msg_id, role, content)
        js_code = f"""
        var element = document.getElementById('{msg_id}');
        element.innerHTML = `{styled_content}`;
        window.scrollTo(0, document.body.scrollHeight);
        """
        self.chat_display.page().runJavaScript(js_code)


if __name__ == "__main__":
    import dotenv

    key_location = Path(ROOT, ".env")
    dotenv.load_dotenv(key_location)

    app = QApplication([])

    model = "openai/gpt-3.5-turbo-0301"
    model = "openai/gpt-4"

    test_dir = Path(ROOT, "tests", "working_delete")
    controller = Controller(test_dir)
    bot_name = "mistral"
    model = "mistralai/mistral-7b-instruct"
    controller.add_bot(bot_name)
    controller.update_bot(bot_name, model=model)
    
    model = "meta-llama/codellama-34b-instruct"
    bot_name = "code_llama"
    controller.add_bot(bot_name)
    controller.update_bot(bot_name,model = model)

    controller.start_conversation(bot_name=bot_name)
    convo_widget = ActiveConversationWidget(controller)
    convo_widget.show()
    app.exec()
