
#%%
import reviver.log

from reviver.conversation import Message, Conversation
from reviver.archive import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot, BotGallery
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

def test_bot_gallery_store_retrieve():
    bot1 = Bot("first bot", model="llama_70b",rank=1)
    bot2 = Bot("second bot", model="llama_70b",rank=2)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)
    bots = {bot1.name:bot1,
            bot2.name:bot2}

    bot_gallery = BotGallery(bots)
    archive.store_bot_gallery(bot_gallery)
    bot_gallery_copy = archive.load_bot_gallery()
    assert(bot_gallery==bot_gallery_copy)

    
def test_message_store_retrieve():
    msg = Message(role="user",content= "hello world!")

    archive = get_new_test_archiver()
    archive.store_message(msg)
    msg_copy = archive.get_message(1,1)
    assert(msg == msg_copy)
    
    
def test_messages_store_retrieve():
    msg1 = Message(role="user",content= "hello world!")
    msg2 = Message(role="assistant",content= "sup?")

    messages = {msg1.position:msg1, msg2.position:msg2}

    archive = get_new_test_archiver()
    # archive.store_messages(messages)
    for position, msg in messages.items():
        archive.store_message(msg)
    messages_copy = archive.get_messages(conversation_id=1)

    assert(messages[1] == messages_copy[1])
    assert(messages[2] == messages_copy[2])

def test_convo_store_retrieve():
    
    msg1 = Message(conversation_id=1,position=1, role="user",content= "hello world!")
    msg2 = Message(conversation_id=1,position=2, role="assistant",content= "sup?")

    bot_1 = Bot(1,"test_bot", model="llama_70b", rank=1)
    bot_2 = Bot(2,"test_bot", model="llama_70b", rank=2)

    bot_gallery = BotGallery()
    bot_gallery.add_bot(bot_1)
    bot_gallery.add_bot(bot_2)
    
    convo = Conversation(1, bot=bot_1)

    convo.add_message(msg1)
    convo.add_message(msg2)

    archive = get_new_test_archiver()
    archive.store_conversation(convo)
    convo_copy = archive.get_conversation(convo_id=1, bot_gallery=bot_gallery) 
    logger.info("Confirm that saved and reloaded convo is same as original")
    assert(convo==convo_copy)

def get_new_test_archiver()->Archive:
    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    db_path = Path(test_dir,"reviver.db")
    assert(not db_path.exists())
    archive = Archive(test_dir)
    return archive
    
     
if __name__ == "__main__":
    
    test_archive_init()
    test_bot_store_retrieve()
    test_bot_gallery_store_retrieve()
    # test_message_store_retrieve()
    # test_messages_store_retrieve()
    # test_convo_store_retrieve()

