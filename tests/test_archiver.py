
#%%
import reviver.log

from reviver.conversation import Message, Conversation
from reviver.conversation_manager import ConversationManager
from reviver.archive import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot, BotManager
from reviver.helper import delete_directory_contents
logger = reviver.log.get(__name__)

def test_archive_init():
    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    logger.info("Confirming that directories do not exist")
    
    bots_dir = Path(test_dir, "bots")  
    convo_dir = Path(test_dir, "conversations")

    assert(not bots_dir.exists())
    assert(not convo_dir.exists())

    logger.info("Init archiver ...")
    archiver = Archive(test_dir)
    logger.info("db should now exist...")
    assert(bots_dir.exists())
    assert(convo_dir.exists())


def test_bot_store_retrieve():
    bot1 = Bot("first bot", model="llama_70b",rank=1)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)

    archive.store_bot(bot1)

    bot1_copy = archive.get_bot("first bot")
    assert(bot1 == bot1_copy) 

def test_bot_manager_store_retrieve():
    bot1 = Bot("first bot", model="llama_70b",rank=1)
    bot2 = Bot("second bot", model="llama_70b",rank=2)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)
    bots = {bot1.name:bot1,
            bot2.name:bot2}

    bot_manager = BotManager(bots)
    archive.store_bot_manager(bot_manager)
    bot_manager_copy = archive.get_bot_manager()
    assert(bot_manager==bot_manager_copy)


def test_convo_store_retrieve():
    
    msg1 = Message(role="user",content= "hello world!")
    msg2 = Message(role="assistant",content= "sup?")

    bot_1 = Bot("test_bot", model="llama_70b", rank=1)
    bot_2 = Bot("test_bot2", model="llama_70b", rank=2)
    bots = {bot_1.name:bot_1,
            bot_2.name:bot_2}
    bot_manager = BotManager(bots)
    
    convo = Conversation(bot=bot_1, title="test")

    convo._add_message(msg1)
    convo._add_message(msg2)

    archive = get_new_test_archiver()
    archive.store_conversation(convo)

    convo_copy = archive.get_conversation(convo_title="test", bot_manager=bot_manager)
    assert(convo_copy==convo)


def test_convo_manager_retrieve():
    archive = get_new_test_archiver()
     
    convo_mngr = ConversationManager()
    
    
    bot_manager = BotManager()
    bot_manager.create_new_bot("bot1")
    bot1 = bot_manager.get_bot("bot1")
    convo_mngr.new_active_conversation(bot1)
    convo_mngr.active_conversation.add_user_message("Hello!")

    
    bot_manager.create_new_bot("bot2")
    bot2 = bot_manager.get_bot("bot2")
    convo_mngr.new_active_conversation(bot2)
    convo_mngr.active_conversation.add_user_message("Hello to you as well!")


    archive.store_all_conversations(convo_mngr)

    library_copy = archive.get_conversation_manager(bot_manager)

    assert(library_copy.conversations.keys() == convo_mngr.conversations.keys())

    for key in convo_mngr.conversations.keys():
        assert(convo_mngr.conversations[key]==library_copy.conversations[key])

def get_new_test_archiver()->Archive:
    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)
    return archive

     
if __name__ == "__main__":
    
    test_archive_init()
    test_bot_store_retrieve()
    test_bot_manager_store_retrieve()
    test_convo_store_retrieve()
    test_convo_manager_retrieve()
