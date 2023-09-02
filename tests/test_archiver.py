
#%%
import reviver.logger

logger = reviver.logger.get(__name__)
import datetime
from reviver.conversation import Message, Conversation
from reviver.archiver import Archiver
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot
from reviver.helper import delete_directory_contents
from reviver.user import User

def test_conversation_save_and_load():
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

    loaded_messages = archiver.get_messages(loaded_test_bot, "testing")
    assert(loaded_messages==convo.messages)

    reload_convo = archiver.get_conversation(loaded_test_bot,"testing")

    assert(type(reload_convo)==Conversation)
    assert(convo == reload_convo)

def test_archive_init():
    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    logger.info("Confirming that db does not exist")
    db_path = Path(test_dir,"reviver.db")
    assert(not db_path.exists())
    logger.info("Init archiver without db...")
    archiver = Archiver(test_dir)

    logger.info("db should now exist...")
    del archiver
    assert(not db_path.exists())
    archiver_new = Archiver(test_dir)

def test_bot_store_retrieve():
    bot1 = Bot(1,"first bot", model="llama_70b",rank=1)
    # bot2 = Bot(2,"first bot", model="llama_70b",rank=2)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archiver(test_dir)

    archive.store_bot(bot1)

    bot1_copy = archive.get_bot(1)
    assert(bot1 == bot1_copy) 

def test_bot_id_list():
    bot1 = Bot(1,"first bot", model="llama_70b",rank=1)
    bot2 = Bot(2,"first bot", model="llama_70b",rank=2)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archiver(test_dir)

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
    archive = Archiver(test_dir)
    archive.store_user(user)
    user_copy = archive.get_user()
    assert(user == user_copy)
    
    
def test_message_store_retrieve():
    msg = Message(conversation_id=1,position=1, role="user",content= "hello world!")

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    db_path = Path(test_dir,"reviver.db")
    assert(not db_path.exists())

    archive = Archiver(test_dir)
    archive.store_message(msg)
    msg_copy = archive.get_message(1,1)
    assert(msg == msg_copy)
    
    
def test_messages_store_retrieve():
    msg1 = Message(conversation_id=1,position=1, role="user",content= "hello world!")
    msg2 = Message(conversation_id=1,position=2, role="assistant",content= "sup?")

    messages = {msg1.position:msg1, msg2.position:msg2}


    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    db_path = Path(test_dir,"reviver.db")
    assert(not db_path.exists())

    archive = Archiver(test_dir)
    archive.store_messages(messages)
    messages_copy = archive.get_messages(conversation_id=1)

    assert(messages[1] == messages_copy[1])
    assert(messages[2] == messages_copy[2])
    
    
     
if __name__ == "__main__":
    
    # test_conversation_save_and_load()
    test_archive_init()
    test_bot_store_retrieve()
    test_bot_id_list()
    test_user_store_retrieve()
    test_message_store_retrieve()
    test_messages_store_retrieve()