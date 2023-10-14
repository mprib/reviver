from PySide6.QtWidgets import (
    QTextEdit,
    QPushButton,
    QApplication,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtWebEngineWidgets import QWebEngineView

# from reviver.conversation import Message, Conversation
# from reviver.bot import Bot
from reviver.controller import Controller
from pathlib import Path
from reviver import ROOT
from reviver.gui.html_styler import style_message
import reviver.log

log = reviver.log.get(__name__)


class ActiveConversationWidget(QWidget):
    """
    A window to the active conversation in the controller layer
    """

    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.chat_display = QWebEngineView()
        self.text_entry = QTextEdit()
        self.send_text = QPushButton("&send")

        self.place_widgets()
        self.connect_widgets()
        self.display_active_conversation()

    def display_active_conversation(self):
        self.chat_display.setHtml(self.controller.get_active_conversation_html())

    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.chat_display)
        self.layout().addWidget(self.text_entry)
        self.layout().addWidget(self.send_text)

    def connect_widgets(self):
        self.send_text.clicked.connect(self.send_user_message)
        # self.controller.message_complete.connect(self.add_message)
        self.controller.message_added.connect(self.add_message)
        self.controller.message_updated.connect(self.update_message)
        self.controller.new_active_conversation.connect(self.display_active_conversation)

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
    model = "meta-llama/codellama-34b-instruct"
    model = "openai/gpt-4"
    model = "mistralai/mistral-7b-instruct"

    test_dir = Path(ROOT, "tests", "working_delete")
    controller = Controller(test_dir)
    bot_name = "test_bot"
    controller.add_bot(bot_name)
    controller.update_bot(bot_name, model=model)
    controller.start_conversation(bot_name=bot_name)
    convo_widget = ActiveConversationWidget(controller)
    convo_widget.show()
    app.exec()
