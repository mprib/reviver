#%%
import reviver.log

from reviver.archive import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot, BotManager
from reviver.helper import delete_directory_contents
log = reviver.log.get(__name__)

def test_bot_creation():
    
    bot1 = Bot("first bot", model="llama_70b",rank=1)

    test_dir = Path(ROOT, "tests", "working_delete")
    delete_directory_contents(test_dir)
    archive = Archive(test_dir)

    archive.store_bot(bot1)
    bot_copy = archive.get_bot(bot1.name)
    assert(bot1==bot_copy)

def test_bot_ranking():
    bot_manager = BotManager()
    bot_manager.create_new_bot("test1")

    bot1 = bot_manager.get_bot("test1")
    assert(bot1.rank==1)
    bot_manager.create_new_bot("test2")
    bot2 = bot_manager.get_bot("test2")
    assert(bot1.rank==2)
    assert(bot2.rank==1)

    bot_manager.create_new_bot("test3")
    bot3 = bot_manager.get_bot("test3")
    
    sorted_bots = bot_manager.get_ranked_bots()
    assert(sorted_bots==[bot3, bot2, bot1])   

    assert(bot1.rank==3)
    assert(bot2.rank==2)
    assert(bot3.rank==1)

    # there should be no change if trying to lower worst or raise beset
    bot_manager.lower_rank(bot1)
    assert(bot1.rank==3)
    assert(bot2.rank==2)
    assert(bot3.rank==1)

    bot_manager.raise_rank(bot3)
    assert(bot1.rank==3)
    assert(bot2.rank==2)
    assert(bot3.rank==1)
    
    # this should change something 
    bot_manager.lower_rank(bot2)
    assert(bot1.rank==2)
    assert(bot2.rank==3)
    assert(bot3.rank==1)

    # as should this
    bot_manager.raise_rank(bot1)
    assert(bot1.rank==1)
    assert(bot2.rank==3)
    assert(bot3.rank==2)
     

def get_four_bot_manager():
    bot_manager = BotManager()
    bot_manager.create_new_bot("test1")
    bot_manager.create_new_bot("test2")
    bot_manager.create_new_bot("test3")
    bot_manager.create_new_bot("test4")
    
    return bot_manager


def test_move_to_higher():
    log.info("Running test_move_to_higher...")
    bot_manager = get_four_bot_manager()
    
    bot1 = bot_manager.get_bot("test1")
    bot2 = bot_manager.get_bot("test2")
    bot3 = bot_manager.get_bot("test3")
    bot4 = bot_manager.get_bot("test4")

    # Check initial ranks
    assert(bot1.rank==4)
    assert(bot2.rank==3)
    assert(bot3.rank==2)
    assert(bot4.rank==1)

    # Move bot1 to rank 2
    bot_manager.move_bot(4, 2)
    assert(bot1.rank==2)
    assert(bot2.rank==4)
    assert(bot3.rank==3)
    assert(bot4.rank==1)

    # Move bot2 to rank 1
    bot_manager.move_bot(4, 1)
    assert(bot1.rank==3)
    assert(bot2.rank==1)
    assert(bot3.rank==4)
    assert(bot4.rank==2)

    log.info("test_move_to_higher passed successfully.")

def test_move_to_lower():
    log.info("Running test_move_to_lower...")
    bot_manager = get_four_bot_manager()
    
    bot1 = bot_manager.get_bot("test1")
    bot2 = bot_manager.get_bot("test2")
    bot3 = bot_manager.get_bot("test3")
    bot4 = bot_manager.get_bot("test4")

    # Check initial ranks
    assert(bot1.rank==4)
    assert(bot2.rank==3)
    assert(bot3.rank==2)
    assert(bot4.rank==1)

    # Move bot4 to rank 3
    bot_manager.move_bot(1, 3)
    assert(bot1.rank==4)
    assert(bot2.rank==2)
    assert(bot3.rank==1)
    assert(bot4.rank==3)

    # Move bot3 to rank 4
    bot_manager.move_bot(1, 4)
    assert(bot1.rank==3)
    assert(bot2.rank==1)
    assert(bot3.rank==4)
    assert(bot4.rank==2)

    log.info("test_move_to_lower passed successfully.")

if __name__ == "__main__":
    test_bot_creation()
    test_bot_ranking()
    test_move_to_higher()
    test_move_to_lower()
      