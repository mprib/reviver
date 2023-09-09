import sys
from typing import Optional
import PySide6.QtCore
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QVBoxLayout,QHBoxLayout, QWidget, QLabel, QPushButton
from PySide6.QtGui import QGuiApplication
from markdown import markdown
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name,guess_lexer
from pygments.formatters import HtmlFormatter
import reviver.logger
log = reviver.logger.get(__name__)


class CodeWidget(QWidget):
    def __init__(self, raw_code):
        super().__init__()

        self.code_block = CodeBlock(raw_code)

        self.lang_label = QLabel()
        self.lang_label.setText(self.code_block.language)
        self.copy_btn = QPushButton("Copy") 
        self.copy_btn.setFixedSize(self.copy_btn.sizeHint())
        self.place_widgets()
        self.connect_widgets()
        
    def place_widgets(self):
        
        self.setLayout(QVBoxLayout())
        self.top_banner = QHBoxLayout()
        self.top_banner.addWidget(self.lang_label)
        self.top_banner.addWidget(self.copy_btn)
        self.layout().addLayout(self.top_banner)
        self.layout().addWidget(self.code_block)

        
    def connect_widgets(self):
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        
    def copy_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.code_block.code)

class CodeBlock(QWebEngineView):
    def __init__(self, raw_code:str):
        super().__init__()
        self.html_formatter = HtmlFormatter()
        self.html_formatter = HtmlFormatter(full=True, style="monokai")
        
        lexer = get_lexer(raw_code)        
        code = get_code(raw_code)

        self.code = code

        highlighted = highlight(code, lexer, self.html_formatter)
        self.setHtml(highlighted)
        
        self.lang_label = QLabel()
        self.language = lexer.name
        self.view = QWebEngineView()
        
        self.place_widgets()

    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        
        self.layout().addWidget
        pass    
    
    def display_markdown(self, md_text):
        html = markdown(md_text)
        self.setHtml(html)

def get_lexer(raw_text):
    
    # if there is a language provided grab it
    # looking to get word immediately after ``` and before new line
    split_text = raw_text.split("\n",maxsplit=1)
    
    potential_language = split_text[0].replace(" ","")
    code = split_text[1]
    try:
        lexer = get_lexer_by_name(potential_language)
        log.info(f"Successfully match lexer to {potential_language}: {lexer}")
    except ClassNotFound as e: 
        log.warning(f"Error {e} raised....guessing lexer")
        lexer = guess_lexer(code)
        log.warning(f"Gessing that lexer is {lexer}")


    return lexer
    # if first_word in
   
def get_code(raw_text):
    
    # if there is a language provided grab it
    # looking to get word immediately after ``` and before new line
    split_text = raw_text.split("\n",maxsplit=1)
    
    return split_text[1]

if __name__== "__main__":

    code = """python
import sys
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class MarkdownViewer(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.html_formatter = HtmlFormatter()

    def display_markdown(self, md_text):
        html = markdown(md_text)
        self.setHtml(html)

    def display_code(self, code, language):
        lexer = get_lexer_by_name(language)
        highlighted = highlight(code, lexer, self.html_formatter)
        self.setHtml(highlighted)

app = QApplication(sys.argv)
viewer = MarkdownViewer()

# Display some markdown
viewer.display_markdown("# Hello, World!")

# Display some Python code with syntax highlighting
viewer.display_code("print('Hello, World!')", "python")

viewer.show()
sys.exit(app.exec()) 
    
    """
    app = QApplication(sys.argv)
    # viewer = CodeBlock(code)
    full_viewer = CodeWidget(code)

    full_viewer.show()
    sys.exit(app.exec())
    
    