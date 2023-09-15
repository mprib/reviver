import sys
from typing import Optional
from PySide6.QtWidgets import QFileDialog, QWidget, QTextEdit, QMainWindow, QVBoxLayout, QPushButton,QApplication, QMenuBar
from PySide6.QtGui import QIcon, QAction, QKeySequence, QShortcut
from reviver import APP_DIR, USER_DIR, REVIVER_SETTINGS
from pathlib import Path
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
        
        log.info(f"Reviver Settings are {REVIVER_SETTINGS}")

    def place_widgets(self):
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def connect_widgets(self):
        self.menu.action_new.triggered.connect(self.create_new_archive)


    def create_new_archive(self):
        dialog = QFileDialog()
        new_directory = QFileDialog.getExistingDirectory(parent=None, 
                                                     caption='Select a folder:', 
                                                     dir=str(USER_DIR), 
                                                     options=QFileDialog.ShowDirsOnly)
        if new_directory:
            log.info(("Creating new project in :", new_directory))
            self.add_archive_to_recent(new_directory)
            self.load_archive(new_directory)
        

    def add_archive_to_recent(self, archive_dir:Path):
        REVIVER_SETTINGS["recent_archives"] += [str(archive_dir)]
        log.info(f"recent archives updated to: {REVIVER_SETTINGS['recent_archives']}")

    def load_archive(self, archive_dir:Path):
        pass
    
class MainMenus(QMenuBar):
    def __init__(self, parent):
        super(MainMenus, self).__init__(parent)
        self.file_menu = self.addMenu("&File")
        self.view_menu = self.addMenu("&View")

        # File Menu
        self.action_new = QAction("&New Archive", self)
        self.file_menu.addAction(self.action_new)

        self.action_open = QAction("&Open Archive", self)
        self.file_menu.addAction(self.action_open)
        
        self.action_open_recent = QAction("Open &Recent Archive", self)
        self.file_menu.addAction(self.action_open_recent)

        # View Menu




if __name__=="__main__":
    
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()