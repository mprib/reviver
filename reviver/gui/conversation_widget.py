from typing import Optional
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidget,QPushButton, QListWidgetItem, QVBoxLayout, QWidget, QHBoxLayout
from reviver.controller import Controller
from reviver.gui.active_conversation_widget import ActiveConversationWidget
class ConversationListView(QWidget):
    def __init__(self, controller:Controller):
        super().__init__()
        self.controller = controller
        self.list_widget = QListWidget()
        self.new_convo_btn = QPushButton("New Conversation")  # not yet implemented

        self.place_widgets()
        self.connect_widgets()
        self.update_conversation_list()
        # Connect the current item changed signal to update the active conversation
        self.list_widget.currentItemChanged.connect(self.update_active_conversation)
    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.list_widget)
        self.layout().addWidget(self.new_convo_btn) 

    def connect_widgets(self):
        self.new_convo_btn.clicked.connect(self.controller.new_active_conversation)
        pass
    
     
    def update_conversation_list(self):
        # Clear the list widget
        self.list_widget.clear()

        # Get the list of conversations
        conversations = self.controller.get_conversation_list()

        # Add each conversation to the list widget
        for conversation in conversations:
            item = QListWidgetItem(conversation)
            self.list_widget.addItem(item)

        # Connect the item clicked signal to set the active conversation
        self.list_widget.itemClicked.connect(self.set_active_conversation)

    def set_active_conversation(self, item):
        conversation_title = item.text()
        self.controller.set_active_conversation(conversation_title)

    @Slot(QListWidgetItem, QListWidgetItem)
    def update_active_conversation(self, current: QListWidgetItem, previous: QListWidgetItem):
        if current is not None:
            conversation_title = current.text()
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

    test_dir = Path(ROOT, "tests", "working_delete")
    controller = Controller(test_dir)
    bot_name = "test_bot"
    controller.add_bot(bot_name)
    controller.update_bot(bot_name, model=model)
    controller.start_conversation(bot_name=bot_name)
    # list_view = ConversationListView(controller)
    
    convo_widget = ConversationWidget(controller)
    convo_widget.show()
    app.exec()
