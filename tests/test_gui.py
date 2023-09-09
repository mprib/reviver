

from reviver.user import User
from reviver.bot import Bot
from reviver.conversation import Conversation, Message
from reviver import ROOT
from pathlib import Path
from queue import Queue

import sys
import reviver.logger
log = reviver.logger.get(__name__)

from reviver.gui.chat_bubble import get_text_code_blocks, starts_with_code



def test_starts_with_code():
    
    code_first = """```python
    print('hello world')
    ```
    
    This is a python program
    
    """
    assert(starts_with_code(code_first)==True)    

    get_text_code_blocks(code_first)
    

    text_first = """
    
    ```python
    print('hello world')
    ```
    
    This is a python program
    
    """

    assert(starts_with_code(text_first)==False)    
    

def test_split_code():
    pass
    
if __name__=="__main__":
    test_starts_with_code()