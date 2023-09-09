import sys
from markdown import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import html
from reviver.conversation import Message

import reviver.logger
log = reviver.logger.get(__name__)

CONTENT_CSS = """
<style>
body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f8f8;
  padding: 1em;
}

h1 {
  font-size: 1.5em; 
  color: #444;
}

h2, h3, h4, h5, h6 {
  color: #444;
}

a {
  color: #0645ad;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code, pre {
  font-family: 'ui-monospace', 'Cascadia Mono', 'Segoe UI Mono', 'Liberation Mono', Menlo, Monaco, Consolas, monospace;
  border-radius: 3px;
  padding: 0.2em 0.4em;
}

pre {
  padding: 1em;
  overflow: auto;
}

pre code {
  background: none;
  border: none;
  padding: 0
</style>
"""

class MessageBlock(QWebEngineView):
    def __init__(self, message:Message):
        super().__init__()
        self.message = message        
        plain_html = convert_markdown_to_html(self.message.content) 
        self.html = style_code_blocks(plain_html)
        self.setHtml(self.html) 
        
def convert_markdown_to_html(input_text):
    html_version = markdown(input_text, extensions=['fenced_code'])
    return html_version

def style_code_blocks(html):
    soup = BeautifulSoup(html, 'html.parser')

    formatter = HtmlFormatter(style='monokai', full=False, cssstyles='overflow:auto;')

    css = formatter.get_style_defs('.highlight')

    for block in soup.find_all('code'):
        language = block.get('class', [None])[0]
        if language is not None:
            language = language[9:]  # remove 'language-' prefix
        code = block.string

        if language is None:
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(language)

        highlighted_code = highlight(code, lexer, formatter)
        block.string.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))
    # Add the CSS to the beginning of the HTML string
    return f'{CONTENT_CSS}<style>{css}</style>' + str(soup)

if __name__=="__main__":
    app = QApplication([])
    


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

# comment
def display_html_in_qwebengineview(html_content):
    app = QApplication([])
    view = QWebEngineView()
    unescaped_html = html.unescape(html_content)
    view.setHtml(unescaped_html)
    view.show()
    sys.exit(app.exec())
```

#why do I even care?
    
The story of stuff and things. 

This is something that I'm going to *emphasize*. I don't really know what to do about that.

Oh and here's a link [googl](www.google.com)

- this is a point
- here is anotehr one

- and again  
"""
    msg = Message(1, "user", content=content,position=1)

    block = MessageBlock(msg)
    block.show()
    
    sys.exit(app.exec())