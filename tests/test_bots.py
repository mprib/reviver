#%%
import reviver.log

from reviver.archive import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot, BotGallery
from reviver.helper import delete_directory_contents
logger = reviver.log.get(__name__)

def test_bot_creation():
    
    bot1 = Bot("first bot", model="llama_70b",rank=1)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)

    archive.store_bot(bot1)
    bot_copy = archive.get_bot(bot1.name)
    assert(bot1==bot_copy)

def test_bot_ranking():
    bot_gallery = BotGallery()
    bot_gallery.create_new_bot("test1")

    bot1 = bot_gallery.get_bot("test1")
    assert(bot1.rank==1)
    bot_gallery.create_new_bot("test2")
    bot2 = bot_gallery.get_bot("test2")
    assert(bot1.rank==2)
    assert(bot2.rank==1)

    bot_gallery.create_new_bot("test3")
    bot3 = bot_gallery.get_bot("test3")
    
    sorted_bots = bot_gallery.get_ranked_bots()
    assert(sorted_bots==[bot3, bot2, bot1])   

    assert(bot1.rank==3)
    assert(bot2.rank==2)
    assert(bot3.rank==1)

    # there should be no change if trying to lower worst or raise beset
    bot_gallery.lower_rank(bot1)
    assert(bot1.rank==3)
    assert(bot2.rank==2)
    assert(bot3.rank==1)

    bot_gallery.raise_rank(bot3)
    assert(bot1.rank==3)
    assert(bot2.rank==2)
    assert(bot3.rank==1)
    
    # this should change something 
    bot_gallery.lower_rank(bot2)
    assert(bot1.rank==2)
    assert(bot2.rank==3)
    assert(bot3.rank==1)
# %%

    # as should this
    bot_gallery.raise_rank(bot1)
    assert(bot1.rank==1)
    assert(bot2.rank==3)
    assert(bot3.rank==2)
    
    
    
    

    
if __name__ == "__main__":
    test_bot_creation()
    test_bot_ranking()