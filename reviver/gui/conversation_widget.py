from typing import Optional

from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtWidgets import QListWidget,QPushButton, QListWidgetItem, QVBoxLayout, QWidget, QHBoxLayout
from reviver.controller import Controller
from reviver.gui.active_conversation_widget import ActiveConversationWidget
import reviver.log
log = reviver.log.get(__name__)

class MyListWidget(QListWidget):
    """
    Needed to make list interactions more stable for both scrolling an clicking
    Single selection signal: itemClicked
    """
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
            self.itemClicked.emit(self.currentItem())

class ConversationListView(QWidget):
    def __init__(self, controller:Controller):
        super().__init__()
        self.controller = controller
        self.list_widget = MyListWidget()
        self.new_convo_btn = QPushButton("New Conversation")  # not yet implemented

        self.place_widgets()
        self.connect_widgets()
        self.refresh()

    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.list_widget)
        self.layout().addWidget(self.new_convo_btn) 

    def connect_widgets(self):
        # Connect the item clicked signal to set the active conversation
        self.list_widget.itemClicked.connect(self.set_active_conversation)
        self.controller.new_active_conversation.connect(self.refresh) 
        self.new_convo_btn.clicked.connect(self.start_new_convo_with_active_bot)

    def start_new_convo_with_active_bot(self):
        bot_name = self.controller.get_active_bot_name()
        log.info(f"Starting new conversation with active bot: {bot_name}") 
        self.controller.start_conversation(bot_name)

    def refresh(self):
        # Clear the list widget
        self.list_widget.clear()

        # Get the list of conversations
        conversations = self.controller.get_conversation_list()

        # Add each conversation to the list widget
        for conversation in conversations:
            item = QListWidgetItem(conversation)
            self.list_widget.addItem(item)

        conversation_title = self.controller.get_active_conversation_title()

        items = self.list_widget.findItems(conversation_title, Qt.MatchExactly)
        if items:
            log.info(f"Attempting to set highlighted list item to {conversation_title}")
            self.list_widget.setCurrentItem(items[0])        

        
    def set_active_conversation(self, item):
        if item is not None:
            conversation_title = item.text()
            log.info(f"Attempting to set active conversation to {conversation_title}")
            self.controller.set_active_conversation(conversation_title)


class ConversationWidget(QWidget):
    def __init__(self, controller:Controller):
        super().__init__()
        self.controller = controller
        
        self.convo_list = ConversationListView(self.controller)
        self.active_convo = ActiveConversationWidget(self.controller)
        
        self.place_widgets()
        self.connect_widgets()
        
    def place_widgets(self):
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.convo_list)
        self.layout().addWidget(self.active_convo)
    
    def connect_widgets(self):
        pass
    
 

        
if __name__ == "__main__":
    import dotenv
    from PySide6.QtWidgets import QApplication
    from pathlib import Path
    from reviver.controller import Controller
    from reviver import ROOT

    key_location = Path(ROOT, ".env")
    dotenv.load_dotenv(key_location)

    app = QApplication([])

    model = "openai/gpt-3.5-turbo-0301"
    model = "meta-llama/codellama-34b-instruct"
    model = "openai/gpt-4"
    model = "mistralai/mistral-7b-instruct"

    test_dir = Path(Path.home(), "reviver")
    # test_dir = Path(ROOT, "tests", "working_delete")
    controller = Controller(test_dir)
    # bot_name = "test_bot"
    # controller.add_bot(bot_name)
    # controller.update_bot(bot_name, model=model)
    # controller.start_conversation(bot_name=bot_name)
    # list_view = ConversationListView(controller)
    
    convo_widget = ConversationWidget(controller)
    convo_widget.show()
    app.exec()
