
#%%
import reviver.logger

from reviver.conversation import Message, Conversation
from reviver.archiver import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot, BotGallery
from reviver.helper import delete_directory_contents
from reviver.user import User
logger = reviver.logger.get(__name__)

def test_archive_init():
    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    logger.info("Confirming that db does not exist")
    db_path = Path(test_dir,"reviver.db")
    assert(not db_path.exists())
    logger.info("Init archiver without db...")
    archiver = Archive(test_dir)

    logger.info("db should now exist...")
    del archiver
    assert(db_path.exists())
    archiver_new = Archive(test_dir)

def test_bot_store_retrieve():
    bot1 = Bot(1,"first bot", model="llama_70b",rank=1)
    # bot2 = Bot(2,"first bot", model="llama_70b",rank=2)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)

    archive.store_bot(bot1)

    bot1_copy = archive.get_bot(1)
    assert(bot1 == bot1_copy) 

def test_bot_id_list():
    bot1 = Bot(1,"first bot", model="llama_70b",rank=1)
    bot2 = Bot(2,"first bot", model="llama_70b",rank=2)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)

    archive.store_bot(bot1)
    archive.store_bot(bot2)

    id_list = archive.get_bot_list()
    assert(id_list == [1,2]) 
    
def test_user_store_retrieve():
    user = User(name= "UserName", key_location="")
     
    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    db_path = Path(test_dir,"reviver.db")
    assert(not db_path.exists())
    archive = Archive(test_dir)
    archive.store_user(user)
    user_copy = archive.get_user()
    assert(user == user_copy)
    
    
def test_message_store_retrieve():
    msg = Message(conversation_id=1,position=1, role="user",content= "hello world!")

    archive = get_new_test_archiver()
    archive.store_message(msg)
    msg_copy = archive.get_message(1,1)
    assert(msg == msg_copy)
    
    
def test_messages_store_retrieve():
    msg1 = Message(conversation_id=1,position=1, role="user",content= "hello world!")
    msg2 = Message(conversation_id=1,position=2, role="assistant",content= "sup?")

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
    
    user = User("TestUser", "C:/keys.toml")
    convo = Conversation(1,bot=bot_1)

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
    test_bot_id_list()
    test_user_store_retrieve()
    test_message_store_retrieve()
    test_messages_store_retrieve()
    test_convo_store_retrieve()

