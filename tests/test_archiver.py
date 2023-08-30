
#%%
import reviver.logger

logger = reviver.logger.get(__name__)
from reviver.conversation import Message, Conversation
from reviver.archiver import Archiver
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot
from reviver.helper import delete_directory_contents

def test_archiver_save_and_load():
    test_bot = Bot(name = "test_bot", model="meta-llama/llama-2-13b-chat")

    convo = Conversation(bot=test_bot)
    
    msg1 = Message(role="user", content="This is a test")
    msg2 = Message(role="assistant", content="I'm just here to help.")


    convo.add_message(msg1)
    convo.add_message(msg2)
    
    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)

    archiver = Archiver(test_dir)
    archiver.store_conversation(convo)

    loaded_test_bot = archiver.get_bot("test_bot","testing")
    assert(test_bot==loaded_test_bot)

    loaded_messages = archiver.get_messages_from_toml(loaded_test_bot, "testing")
    assert(loaded_messages==convo.messages)

    reload_convo = archiver.get_conversation(loaded_test_bot,"testing")

    assert(type(reload_convo)==Conversation)
    assert(convo == reload_convo)

if __name__ == "__main__":
    
    test_archiver_save_and_load()

