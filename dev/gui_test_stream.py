import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QTimer, Slot

html = """
<!DOCTYPE html>
<html>
<body>

<h1 style="color:blue;">Welcome to My Web Page</h1>

<p id="demo"></p>

</body>
</html>
"""

class WebView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.append_word)
        self.timer.start(1000)  # Starts the timer to call append_word every second
        self.setHtml(html)
        self.word_index = 0
        self.word_list = ["Hello", "World", "This", "is", "a", "QWebEngineView", "demo"]

    @Slot()
    def append_word(self):
        if self.word_index < len(self.word_list):
            self.page().runJavaScript('document.getElementById("demo").innerHTML += "{0} ";'.format(self.word_list[self.word_index]))
            self.word_index += 1

app = QApplication(sys.argv)

web = WebView()
web.show()

sys.exit(app.exec())