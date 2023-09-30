from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
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

class BotGalleryWidget(QListWidget):
    def __init__(self, bot_gallery:BotGallery, spec_sheet:ModelSpecSheet):
        super().__init__()
        self.gallery = bot_gallery
        self.spec_sheet = spec_sheet

        self.list_widget = QListWidget()
        self.active_bot = self.gallery.get_bot_by_rank(1)
        self.bot_widget = BotWidget(self.active_bot, spec_sheet)

        self.add_button = QPushButton("Add bot")
        self.remove_button = QPushButton("Remove bot")

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
        self.left_half.addLayout(self.list_buttons)
        
        self.layout().addLayout(self.left_half)
        self.layout().addWidget(self.bot_widget)
    
    
    def connect_widgets(self):

        self.add_button.clicked.connect(self.add_bot)
        self.remove_button.clicked.connect(self.remove_bot)
        self.list_widget.itemClicked.connect(self.update_bot_widget)
    
    def load_bots(self):
        self.list_widget.clear()
        for bot in self.gallery.get_ranked_bots():
            self.list_widget.addItem(bot.name)

    def add_bot(self):
        name, ok = QInputDialog.getText(self, "Add bot", "Enter bot name:")
        if ok and name:
            self.gallery.create_new_bot(name, "model")
            self.load_bots()

    def remove_bot(self):
        item = self.list_widget.currentItem()
        if item:
            self.gallery.remove_bot(item.text())
            self.load_bots()

    def update_bot_widget(self, item):
        log.info(f"Updating bot widget to reflect {item.text()}")
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
