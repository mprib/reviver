import sys
from PySide6.QtWidgets import QWidget, QTextEdit, QMainWindow, QVBoxLayout, QPushButton


class CollapsibleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.collapsed = False
        self.toggle_button = QPushButton("Toggle Logger", self)
        self.toggle_button.clicked.connect(self.toggle)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.toggle_button)
        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

    def toggle(self):
        self.collapsed = not self.collapsed
        self.text_edit.setHidden(self.collapsed)
        if self.collapsed:
            self.toggle_button.setText("Show Logger")
        else:
            self.toggle_button.setText("Hide Logger")


class MainWindow(QMainWindow):
    def __init__(
        self,
    ):
        super().__init__()

        self.setWindowTitle("reviver")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget(self)
        self.collapsible_widget = CollapsibleWidget(self)

        self.place_widgets()
        self.connect_widgets()

    def place_widgets(self):
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.layout.addWidget(self.collapsible_widget)

    def connect_widgets(self):
        pass
