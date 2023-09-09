"""
Display a single chat 


"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
import re
import html
from PySide6.QtWebEngineWidgets import QWebEngineView
from reviver.conversation import Message
import reviver.logger
import markdown

log = reviver.logger.get(__name__)

class Message_Content(QWidget):
    def __init__(self, message: Message, parent=None):
        super().__init__(parent)

        # Create the layout
        layout = QVBoxLayout(self)

        # Create the QWebEngineView for the content
        self.content_view = QWebEngineView(self)

        # Add widgets to the layout
        layout.addWidget(self.content_view)

        # Set the message
        self.set_message(message)

    def set_message(self, message: Message):

        # Convert markdown content to HTML
        html_content = markdown.markdown(message.content, extensions=["fenced_code"])
        log.info(f"Converted html is: {html_content}")
        # Set the role label and the content view
        # self.role_label.setText(f"{message.role}")
        self.content_view.setHtml(html_content)
        
        
        

   
    
def get_text_code_blocks(raw_text:str)->list:
    """
    Provided with the raw content of the message, this will split
    out blocks of text using ``` as a delimiter.
    
    If the raw text starts with ```, it will be padded with a \n
    such that the first entry will always be plain text and
    alternating entries will be code.
    
    ensures that multiple code blocks can exist in a single chat message
    
    """
    pass

def starts_with_code(raw_text:str)->bool:
    if raw_text[0:3] == "```":
        return True
    else:
        return False

if __name__=="__main__":
    
    content = """
    
    This is some basic content. Lets
    just keep this here
    
    for now. 
    
    ```python
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    print("hello world")
    
    ```
    
    
    """
    
    app = QApplication()
    msg = Message(1, "user", content=content,position=1)

    bubble = Message_Content(msg)
    
    bubble.show()
    app.exec()