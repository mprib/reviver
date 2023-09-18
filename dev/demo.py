from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from reviver.conversation import Message, Conversation
from reviver.user import User
from reviver.bot import Bot
from reviver import ROOT
from pathlib import Path
from threading import Thread
from queue import Queue

import sys
import reviver.log
log = reviver.log.get(__name__)


key_location=Path(ROOT, "keys.toml")
user = User(name="Me The User", key_location=key_location)

log.info(user.keys)
model = "jondurbin/airoboros-l2-70b-2.1"
bot = Bot(_id=1,name="rocket_logic", model=model, rank=1)
convo = Conversation(_id = 1, user=user, bot=bot)

def input_worker():
    
    while True:
        log.info("Waiting on content from user...")
        content = input("User:")
        log.info(f"Content just entered: {content}")        
        if content == "quit":
            break

        msg = Message(convo._id, "user", content=content)

        log.info(f"Adding message: {msg}")
        convo.add_message(msg)

        # web_view.setHtml(convo.as_styled_html())
        stream_q = Queue()
        convo.generate_next_message(stream_q)

        while True:
            word = stream_q.get()
            if word is None:
                break
            else:
                sys.stdout.write(word)    

input_thread = Thread(target=input_worker, args=[], daemon=True)    
input_thread.start()


