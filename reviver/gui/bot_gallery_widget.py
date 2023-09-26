from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QTabWidget,QTabBar, QLabel, QInputDialog, QListWidget, QVBoxLayout, QWidget
from reviver.bot import BotGallery

class BotTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def moveTab(self, fromIndex, toIndex):
        super().moveTab(fromIndex, toIndex)
        self.parent().handleTabMove(fromIndex, toIndex)

    
class BotTabWidget(QTabWidget):
    def __init__(self, bot_gallery):
        super().__init__()
        self.gallery = bot_gallery

        self.setTabBar(BotTabBar(self))

        # layout = QVBoxLayout(self)
        # layout.addWidget(self.tabWidget)

        self.initUI()

    def initUI(self):
        self.setMovable(True)
        
        for bot in self.gallery.get_ranked_bots():
            tab = QWidget()
            layout = QVBoxLayout(tab)
            layout.addWidget(QLabel(f"Bot name: {bot.name}"))
            layout.addWidget(QLabel(f"Bot model: {bot.model}"))
            layout.addWidget(QLabel(f"Bot rank: {bot.rank}"))
            self.addTab(tab, bot.name)

if __name__ =="__main__":
    # Assuming "gallery" is an instance of BotGallery
    gallery = BotGallery()
    gallery.create_new_bot("Bot1", "model1")
    gallery.create_new_bot("Bot2", "model2")
    gallery.create_new_bot("Bot3", "model3")

    app = QApplication([])
    bot_tab_widget = BotTabWidget(gallery)
    bot_tab_widget.show()
    app.exec()
