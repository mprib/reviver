import logging
from PySide6.QtCore import QObject, Signal
from pathlib import Path
import sys
import os
from reviver import APP_DIR


class QtHandler(logging.Handler):
    """
    Method adapted from: 
    https://stackoverflow.com/questions/24469662/how-to-redirect-logger-output-into-pyqt-text-widget 
    """
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record: 
            LogStream.stdout().write(f"{record}")

class LogStream(QObject):
    _stdout = None
    _stderr = None
    new_log_statement = Signal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.new_log_statement.emit(msg)

    @staticmethod
    def stdout():
        if not LogStream._stdout:
            LogStream._stdout = LogStream()
            sys.stdout = LogStream._stdout
        return LogStream._stdout

    @staticmethod
    def stderr():
        if not LogStream._stderr:
            LogStream._stderr = LogStream()
            sys.stderr = LogStream._stderr
        return LogStream._stderr

log_format = " %(levelname)8s| %(name)30s| %(lineno)3d|  %(message)s"
formatter = logging.Formatter(log_format)

terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(formatter)

log_path = Path(APP_DIR,"reviver.log")
log_file_handler = logging.FileHandler(log_path, mode="w+")
log_file_handler.setFormatter(formatter)

qt_handler = QtHandler()
qt_handler.setFormatter(formatter)

def get(name):  # as in __name__
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(terminal_handler)
    log.addHandler(log_file_handler)
    log.addHandler(qt_handler)
    
    return log
