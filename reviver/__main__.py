import sys
import os
from PySide6.QtWidgets import QApplication
from pathlib import Path
import reviver.log
from reviver.gui.main import MainWindow
log = reviver.log.get(__name__)

def command_line_launcher():
    run_main()
    
def run_main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    