
from reviver.conversation import Message, Conversation
from reviver.archiver import Archive
from pathlib import Path
from reviver import ROOT, USER_SETTINGS
from reviver.bot import Bot
from reviver.user import User
from reviver.helper import delete_directory_contents
import reviver.logger
from reviver.session import Session
logger = reviver.logger.get(__name__)


def test_session_creation():

    test_dir = Path(ROOT, "tests", "working_delete")    
    delete_directory_contents(test_dir)

    
    session = Session(test_dir)
    
        


if __name__== "__main__":
    test_session_creation()