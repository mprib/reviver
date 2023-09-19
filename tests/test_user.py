

#%%

from reviver.conversation import Message, Conversation
from reviver.archiver import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot
from reviver.user import User
import rtoml
from reviver.helper import delete_directory_contents
import reviver.log
logger = reviver.log.get(__name__)


def test_user_creation_and_load():

    test_dir = Path(ROOT, "tests", "working_delete")    
    delete_directory_contents(test_dir)
    user = User("Test_user")
    logger.info(f"User is :{user}")    

    assert(user.keys is None)
    
    # create test keys database
    key_toml = Path(test_dir, "keys.toml")
    keys = {"OPEN_ROUTER_API_KEY":"sk-or-v1", 
            "WHISPER_API_KEY":"sk-vkJlGN"}
    rtoml.dump(keys,key_toml) 

    assert(key_toml.exists())

    user.dot_env_loc = str(key_toml)
    assert(user.keys == keys)
    
    archive = Archive(test_dir)
    archive.store_user(user)
    
    # load user from database
    archive_copy = Archive(test_dir)
    user_copy = archive_copy.get_user()
    
    assert(user==user_copy)


if __name__== "__main__":
    test_user_creation_and_load()