
from reviver.archive import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot
from reviver.helper import delete_directory_contents
import reviver.log
from reviver.controller import Controller
log = reviver.log.get(__name__)


def test_session_creation():

    test_dir = Path(ROOT, "tests", "working_delete")    
    delete_directory_contents(test_dir)

    
    model = "jondurbin/airoboros-l2-70b-2.1"
    bot = Bot(name="rocket_logic", model=model, rank=1)
    
    archive = Archive(test_dir)

    archive.store_bot(bot)
    del archive

    Controller(test_dir)


    # session.start_conversatin(bot_id=1)
    
        


if __name__== "__main__":
    test_session_creation()