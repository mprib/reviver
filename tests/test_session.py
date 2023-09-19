
from reviver.conversation import Message, Conversation
from reviver.archiver import Archive
from pathlib import Path
from reviver import ROOT, REVIVER_SETTINGS
from reviver.bot import Bot
from reviver.user import User
from reviver.helper import delete_directory_contents
import reviver.log
from reviver.session import Session
log = reviver.log.get(__name__)


def test_session_creation():

    test_dir = Path(ROOT, "tests", "working_delete")    
    delete_directory_contents(test_dir)

    
    key_location=Path(ROOT, "keys.toml")
    user = User(name="Me The User", dot_env_loc=key_location)
    log.info(user.keys)

    log.info(user.keys)
    model = "jondurbin/airoboros-l2-70b-2.1"
    bot = Bot(_id=1,name="rocket_logic", model=model, rank=1)
    
    archive = Archive(test_dir)

    archive.store_user(user)
    archive.store_bot(bot)
    del archive

    session = Session(test_dir)


    # session.start_conversatin(bot_id=1)
    
        


if __name__== "__main__":
    test_session_creation()