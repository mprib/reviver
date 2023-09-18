import reviver.log

logger = reviver.log.get(__name__)
from reviver.conversation import Message, Conversation
from reviver.archiver import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot
from reviver.helper import delete_directory_contents

def test_bot_creation():
    
    bot1 = Bot(1,"first bot", model="llama_70b",rank=1)
    bot2 = Bot(2,"first bot", model="llama_70b",rank=2)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)

    archive.store_bot(bot1)


    
if __name__ == "__main__":
    test_bot_creation()

