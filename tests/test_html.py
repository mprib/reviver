from reviver.conversation import Message, Conversation
from reviver.bot import Bot
from reviver.user import User
import reviver.logger
from bs4 import BeautifulSoup

log = reviver.logger.get(__name__)

content = """
This is some basic content. Lets
just keep this here for now. 
    
```python
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

# This is a heading
    
## Subheading
The story of stuff and things. 
## Subheading 2
then things got worse


# Another Heading

This is something that I'm going to *emphasize*. I don't really know what to do about that.

- this is a point
- here is anotehr one
- and again  
"""
def test_message_to_html():
    
    # user = User(name="Me The User")
    # bot = Bot(_id=1,name="friend", model="random", rank=1)
    # convo = Conversation(_id = 1, user=user, bot=bot)
    msg1 = Message(1, "user", content=content,position=1)
    # msg2 = Message(2, "assistant", content=" This is some *stuff*",position=2)

    soup = BeautifulSoup(msg1.as_html(), 'html.parser')
    log.info(msg1.as_html())

    assert(len(soup.find_all('p'))==4)
    assert(len(soup.find_all('h1'))==2)
    assert(len(soup.find_all('h2'))==2)


def test_conversation_to_html():
    user = User(name="Me The User")
    bot = Bot(_id=1,name="friend", model="random", rank=1)
    convo = Conversation(_id = 1, user=user, bot=bot)
    msg1 = Message(1, "user", content=content,position=1)
    msg2 = Message(2, "assistant", content=" This is some *stuff*",position=2)

    convo.add_message(msg1)
    convo.add_message(msg2)
    
    styled_html = convo.as_styled_html()

    soup = BeautifulSoup(styled_html, "html.parser")
    log.info(styled_html)
    assert(len(soup.find_all('p'))==7)
    assert(len(soup.find_all('code'))==1)
    assert(len(soup.find_all('h1'))==2)
    assert(len(soup.find_all('h2'))==2)

if __name__ == "__main__":
    test_message_to_html()
    test_conversation_to_html()
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication([])

    user = User(name="Me The User")
    bot = Bot(_id=1,name="friend", model="random", rank=1)
    convo = Conversation(_id = 1, user=user, bot=bot)
    msg1 = Message(1, "user", content=content,position=1)
    msg2 = Message(2, "assistant", content=" This is some *stuff*",position=2)
    msg3 = Message(3, "user", content="# heading \n this is another question",position=1)

    convo.add_message(msg1)
    convo.add_message(msg2)
    convo.add_message(msg3)

    web_view = QWebEngineView()
    
    web_view.setHtml(convo.as_styled_html())

    web_view.show() 
    sys.exit(app.exec())