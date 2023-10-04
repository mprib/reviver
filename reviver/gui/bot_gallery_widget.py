from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QInputDialog,
    QListWidget,
    QVBoxLayout,
)
from reviver.gui.bot_widget import BotWidget
from reviver.controller import Controller
import reviver.log

log = reviver.log.get(__name__)


class DraggableListWidget(QListWidget):
    def __init__(self, controller: Controller, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.InternalMove)
        self.controller = controller

    def dropEvent(self, event):
        if event.source() == self:
            source_index = self.currentRow()
            super().dropEvent(event)
            destination_index = self.currentRow()
            self.controller.move_bot(source_index + 1, destination_index + 1)


# In BotGalleryWidget __init__ method
class BotGalleryWidget(QListWidget):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

        self.list_widget = DraggableListWidget(self.controller)

        self.bot_widget = BotWidget(self.controller)

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
        # self.bot_widget.save_button.clicked.connect(self.load_bots)

    def rename_bot(self):
        old_name = self.list_widget.currentItem().text()
        new_name, ok = QInputDialog.getText(self, "Add bot", "Enter bot name:")
        if ok and new_name:
            # confirm that this name is unique
            success = self.controller.rename_bot(old_name, new_name)
            if not success:
                self.launch_duplicate_warning(
                    new_name, f"Cannot rename bot to {new_name}"
                )
            else:
                self.load_bots()
                self.bot_widget.display_bot(new_name)
                # Restore the selection with the new name
                matching_items = self.list_widget.findItems(new_name, Qt.MatchExactly)
                if matching_items:
                    self.list_widget.setCurrentItem(matching_items[0])

    def launch_duplicate_warning(self, name, warning_text):
        log.warning(f"Attempting to create bot using pre-existing name: {name}")
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
        for bot_name in self.controller.get_ranked_bot_names():
            self.list_widget.addItem(bot_name)
            self.list_widget.setCurrentRow(0)

    def add_bot(self):
        name, input_success = QInputDialog.getText(self, "Add bot", "Enter bot name:")
        if input_success and name:
            new_bot_success = self.controller.add_bot(name)
            if new_bot_success:
                log.info(f"New bot created {name}")
                self.load_bots()
                self.list_widget.setCurrentRow(0)
            else:
                self.launch_duplicate_warning(
                    name, f"Cannot create new bot named {name}"
                )

    def remove_bot(self):
        item = self.list_widget.currentItem()
        if item:
            self.controller.remove_bot(item.text())
            self.load_bots()

    def update_bot_widget(self, item):
        if item is not None:
            bot_name = item.text()
            log.info(f"Updating bot widget to display {bot_name}")
            # bot = self.gallery.bots[item.text()]
            # if bot:
            self.bot_widget.display_bot(bot_name)


if __name__ == "__main__":
    from reviver.controller import Controller

    from pathlib import Path

    archive_dir = Path(Path.home(), "reviver")
    controller = Controller(archive_dir)
    controller.add_bot("test_bot")
    app = QApplication()
    bot_gallery_widget = BotGalleryWidget(controller)
    bot_gallery_widget.show()
    app.exec()
