
#%%
import reviver.logger

logger = reviver.logger.get(__name__)
from reviver.conversation import Message, Conversation
from reviver.archiver import Archiver
from pathlib import Path
from reviver import ROOT

def test_archiver_save():

    msg1 = Message(role="user", content="This is a test")
    msg2 = Message(role="assistant", content="I'm just here to help.")

    convo = Conversation()

    convo.add_message(msg1)
    convo.add_message(msg2)
    
    test_dir = Path(ROOT, "tests", "working_delete")
    archiver = Archiver(test_dir)

    archiver.store_conversation(convo)


if __name__ == "__main__":
    
    test_archiver_save()

# %%
