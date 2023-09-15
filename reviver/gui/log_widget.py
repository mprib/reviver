from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QApplication
from PySide6.QtCore import Slot
from reviver.log import LogStream, get
import threading
import time

class LogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

        LogStream.stdout().new_log_statement.connect(self.append_log)

    @Slot(str)
    def append_log(self, text):
        self.text_edit.append(text)

def log_statements():
    logger = get(__name__)
    while True:
        logger.info("Logging statement at: " + time.ctime())
        time.sleep(1)

if __name__ == "__main__":
    app = QApplication([])
    widget = LogWidget()
    widget.show()

    log_thread = threading.Thread(target=log_statements, daemon=True)
    log_thread.start()

    app.exec()