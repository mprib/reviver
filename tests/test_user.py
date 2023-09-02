

#%%
import reviver.logger

logger = reviver.logger.get(__name__)
from reviver.conversation import Message, Conversation
from reviver.archiver import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot
from reviver.user import User
from reviver.helper import delete_directory_contents


def test_user_creation_and_load():
    
    user = User("Test_user")

    bot1 = Bot("New bot", model= "meta-llama/llama-2-70b-chat")
    bot2 = Bot("Second bot", model= "meta-llama/llama-2-70b-chat")
    bot3 = Bot("Third bot", model= "meta-llama/llama-2-70b-chat")

    user.add_bot(bot1)
    user.add_bot(bot2)
    user.add_bot(bot3)

    assert(user.bot_count == 3)


if __name__== "__main__":
    test_user_creation_and_load()