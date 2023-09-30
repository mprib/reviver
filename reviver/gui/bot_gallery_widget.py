from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTabBar,
    QLabel,
    QInputDialog,
    QListWidget,
    QVBoxLayout,
    QWidget,
)
from reviver.bot import BotGallery, Bot
from reviver.gui.bot_widget import BotWidget
from reviver.models_data import ModelSpecSheet
import reviver.log

log = reviver.log.get(__name__)
class DraggableListWidget(QListWidget):
    def __init__(self, bot_gallery, parent=None):
        super().__init__(parent)
        self.bot_gallery = bot_gallery
        self.setDragDropMode(QListWidget.InternalMove)

    def dropEvent(self, event):
        if event.source() == self:
            source_index = self.currentRow()
            super().dropEvent(event)
            destination_index = self.currentRow()
            self.bot_gallery.move_bot(source_index + 1, destination_index + 1)

# In BotGalleryWidget __init__ method
class BotGalleryWidget(QListWidget):
    def __init__(self, bot_gallery:BotGallery, spec_sheet:ModelSpecSheet):
        super().__init__()
        self.gallery = bot_gallery
        self.spec_sheet = spec_sheet

        self.list_widget = DraggableListWidget(self.gallery)
        initial_bot = self.gallery.get_bot_by_rank(1)
        self.bot_widget = BotWidget(initial_bot, spec_sheet)

        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")
        self.rename_button = QPushButton("Rename")

        self.load_bots()
        self.place_widgets()
        self.connect_widgets()
        
    def place_widgets(self):
        self.setLayout(QHBoxLayout())
        self.left_half = QVBoxLayout()

        self.left_half.addWidget(self.list_widget)
                
        self.list_buttons = QHBoxLayout()
        self.list_buttons.addWidget(self.add_button)
        self.list_buttons.addWidget(self.remove_button)
        self.list_buttons.addWidget(self.rename_button)
        self.left_half.addLayout(self.list_buttons)
        
        self.layout().addLayout(self.left_half)
        self.layout().addWidget(self.bot_widget)
    
    
    def connect_widgets(self):

        self.add_button.clicked.connect(self.add_bot)
        self.remove_button.clicked.connect(self.remove_bot)
        self.rename_button.clicked.connect(self.rename_bot)
        self.list_widget.currentItemChanged.connect(self.update_bot_widget)
        self.bot_widget.save_button.clicked.connect(self.load_bots)

    def rename_bot(self):
        new_name, ok = QInputDialog.getText(self, "Add bot", "Enter bot name:")
        if ok and new_name:
            # confirm that this name is unique
            if new_name in self.gallery.bots.keys():
                self.launch_duplicate_warning(new_name, f"Cannot rename bot to {new_name}")
            else:
                old_name = self.bot_widget.bot.name
                self.gallery.rename_bot(old_name,new_name)
                self.bot_widget.load_bot(self.bot_widget.bot)
                self.load_bots()

                # Restore the selection with the new name
                matching_items = self.list_widget.findItems(new_name, Qt.MatchExactly)
                if matching_items:
                    self.list_widget.setCurrentItem(matching_items[0])
 
    def launch_duplicate_warning(self, name, warning_text):
        log.warn(f"Attempting to create bot using pre-existing name: {name}")
        message_box = QMessageBox(parent=self)
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(warning_text)
        message_box.setInformativeText("This bot already exists.")
        message_box.setWindowTitle("Duplicate Bot Attempt")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()
        
        
    def load_bots(self):
        log.info("Loading ranked list of bot gallery.")
        self.list_widget.clear()
        for bot in self.gallery.get_ranked_bots():
            self.list_widget.addItem(bot.name)

    def add_bot(self):
        name, ok = QInputDialog.getText(self, "Add bot", "Enter bot name:")
        if ok and name:
            # confirm that this name is unique
            if name in self.gallery.bots.keys():
                self.launch_duplicate_warning(name, f"Cannot create new bot named {name}")
            else:
                log.info(f"Creating new bot: {name}")
                self.gallery.create_new_bot(name)
                self.load_bots()
                self.list_widget.setCurrentRow(0)

    def remove_bot(self):
        item = self.list_widget.currentItem()
        if item:
            self.gallery.remove_bot(item.text())
            self.load_bots()

    def update_bot_widget(self, item):
        if item is not None:
            log.info(f"Updating bot widget to display {item.text()}")
            bot = self.gallery.bots[item.text()]
            if bot:
                self.bot_widget.load_bot(bot)


if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path
    from os import getenv

    archive_dir = Path(Path.home(), "reviver")
    env_location = Path(archive_dir, ".env")
    load_dotenv(dotenv_path=env_location)
    key = getenv("OPEN_ROUTER_API_KEY")
    spec_sheet = ModelSpecSheet(key)

    # Assuming "gallery" is an instance of BotGallery
    gallery = BotGallery()
    gallery.create_new_bot("Bot1", "model1")
    gallery.create_new_bot("Bot2", "model2")
    gallery.create_new_bot("Bot3", "model3")

    app = QApplication([])
    bot_gallery_widget = BotGalleryWidget(gallery, spec_sheet)
    bot_gallery_widget.show()
    app.exec()
