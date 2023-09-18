from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog


class ArchiveCreator(QWidget):
    """
    Not much to this. Primarily just need a user name and directory target
    This will be launched from the 'New Archive` action on file menu 
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        


if __name__ == "__main__":
    app = QApplication([])
    widget = ArchiveCreator()
    widget.show()
    app.exec()