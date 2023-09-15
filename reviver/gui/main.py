import sys
from typing import Optional
from PySide6.QtWidgets import QWidget, QTextEdit, QMainWindow, QVBoxLayout, QPushButton,QApplication, QMenuBar
from PySide6.QtGui import QIcon, QAction, QKeySequence, QShortcut
from reviver import APP_DIR, USER_DIR, REVIVER_SETTINGS
import reviver.log
log = reviver.log.get(__name__)

class MainWindow(QMainWindow):
    def __init__( self):
        super().__init__()

        self.setWindowTitle("reviver")
        self.setGeometry(100, 100, 800, 600)
        self.menu = MainMenus(self) # what I'm trying to inject into the main window
        self.setMenuBar(self.menu)
        
        self.central_widget = QWidget(self)
        self.place_widgets()
        self.connect_widgets()
        
        log.info(f"User Settings are ")

    def place_widgets(self):
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def connect_widgets(self):
        pass

    
class MainMenus(QMenuBar):
    def __init__(self, parent):
        super(MainMenus, self).__init__(parent)
        self.file_menu = self.addMenu("&File")
        self.view_menu = self.addMenu("&View")

        # File Menu
        self.new_action = QAction("&New Archive", self)
        self.file_menu.addAction(self.new_action)

        self.open_action = QAction("&Open Archive", self)
        self.file_menu.addAction(self.open_action)
        
        self.open_recent_action = QAction("Open &Recent Archive", self)
        self.file_menu.addAction(self.open_recent_action)

        # View Menu




if __name__=="__main__":
    
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()