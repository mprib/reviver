
from reviver.archive import Archive
from pathlib import Path
from reviver import ROOT
from reviver.bot import Bot
from reviver.helper import delete_directory_contents
import reviver.log
from reviver.conversation import Conversation
from reviver.message import Message
from reviver.controller import Controller
log = reviver.log.get(__name__)


def test_controller_creation():

    test_dir = Path(ROOT, "tests", "working_delete")    
    delete_directory_contents(test_dir)

    
    model = "jondurbin/airoboros-l2-70b-2.1"
    bot = Bot(name="rocket_logic", model=model, rank=1)

    # controller is the thing that will create all other objects
    Controller(test_dir)



def test_controller_bot_names():
    test_dir = Path(ROOT, "tests", "working_delete")    
    delete_directory_contents(test_dir)

    controller = Controller(test_dir)
    
    bot_name = "rocket" 
    model = "jondurbin/airoboros-l2-70b-2.1"
    controller.add_bot(bot_name=bot_name)
    
    bot_name = "rocket_2" 
    model = "jondurbin/airoboros-l2-70b-2.1"
    controller.add_bot(bot_name=bot_name)
    
    bot_list = controller.get_ranked_bot_names()     

    assert(bot_list ==["rocket_2", "rocket"])

def test_controller_create_convo():
    test_dir = Path(ROOT, "tests", "working_delete")    
    delete_directory_contents(test_dir)

    controller = Controller(test_dir)
    
    bot_name = "rocket" 
    model = "meta-llama/codellama-34b-instruct"
    controller.add_bot(bot_name=bot_name)
    controller.update_bot(bot_name=bot_name,model=model)
    
    controller.start_conversation(bot_name="rocket")    

    assert(isinstance(controller.convo_manager.active_conversation, Conversation))
    # controller.add_new_user_message("Hello! Can you help me?")    



if __name__== "__main__":
    test_controller_creation()
    test_controller_bot_names()
    test_controller_create_convo()