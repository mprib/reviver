

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

    


if __name__== "__main__":
    test_user_creation_and_load()