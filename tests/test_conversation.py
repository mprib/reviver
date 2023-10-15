import reviver.log

from reviver.conversation import Conversation
from reviver.conversation_manager import ConversationManager
from reviver.message import Message
from reviver.bot import Bot
logger = reviver.log.get(__name__)

def test_conversation_creation():

    msg1 = Message(role="user", content="This is a test")
    msg2 = Message(role="assistant", content="sup?")
    
    bot = Bot(name="test_bot", model = "llama_70b", rank=1, system_prompt="good bot")
    convo = Conversation(title = "New conversation", bot=bot)

    convo._add_message(msg1)
    convo._add_message(msg2)

    logger.info(f"conversation list is {convo.messages_prompt}")
    target_list = [
        {"role": "system", "content": "good bot"},
        {"role": "user", "content": "This is a test"},
        {"role": "assistant", "content": "sup?"},
    ]
    assert convo.messages_prompt == target_list

def test_token_size():
    msg1 = Message(role="user", content="This is a test")
    msg2 = Message(role="assistant", content="This is a test")

    logger.info(f"test message size is {msg1.token_size}")
    assert(msg1.token_size == msg2.token_size)
    
    bot = Bot(name="test_bot", model = "llama_70b", rank = 1, system_prompt="good bot")
    convo = Conversation(title = "New conversation", bot=bot)
    

    system_message = convo.messages[0]
    convo._add_message(msg1)
    convo._add_message(msg2)


    # three messages are in the conversation now, including the system prompt
    assert(convo.token_size == msg1.token_size+msg2.token_size + system_message.token_size)
    logger.info(f"conversation size is {convo.token_size}")


def test_conversation_list_order():
    convo_manager = ConversationManager()

    bot = Bot("test_bot", model="test", rank=1)
    for i in range(5):
        
        convo_manager.new_active_conversation(bot)
        convo_manager.active_conversation.add_user_message(f"Hi bot! This is conversation {i}")
        title = convo_manager.active_conversation.title
        convo_manager.rename_conversation(title, f"Convo {i}")
    

    logger.info("Title order")
    convo_order = []
    for title in convo_manager.get_conversation_list():
        logger.info(title)
        convo_order.append(int(title[-1]))
    
    assert(convo_order == [4,3,2,1,0])
    
    convo_manager.set_active_conversation("Convo 2")
    convo_manager.active_conversation.add_user_message("This is a new message")

    convo_order = []
    for title in convo_manager.get_conversation_list():
        logger.info(title)
        convo_order.append(int(title[-1]))
    assert(convo_order == [2,4,3,1,0])

    logger.info("Title order")
    for title in convo_manager.get_conversation_list():
        logger.info(title)

   
def test_conversation_start():
    """
    starts a couple of conversations and uses the active convo reference to make some changes
    makes sure the conversations are being created and pointed to correctly
    """
    convo_manager = ConversationManager()

    bot = Bot("test_bot", model="test", rank=1)
    convo_manager.new_active_conversation(bot)
    title = convo_manager.active_conversation.title
    convo_manager.rename_conversation(title, "Convo 1")
    
    convo_manager.new_active_conversation(bot)
    title = convo_manager.active_conversation.title
    convo_manager.rename_conversation(title, "Convo 2")

    assert(convo_manager.conversations['Convo 1'] != convo_manager.conversations['Convo 2'])

def test_update_system_prompt():
    good_prompt = "You are a good bot"
    bot = Bot("test_bot", model="test_model", system_prompt=good_prompt,rank=1)    
    convo = Conversation(bot, title="test_convo")
    assert(convo.messages[0].content==good_prompt)
    evil_prompt = "You are an evil bot"
    bot.system_prompt = evil_prompt
    convo.update_system_prompt()
    assert(convo.messages[0].content==evil_prompt)


if __name__ == "__main__":
    # test_conversation_creation()
    # test_token_size()
    # test_conversation_list_order()
    # test_conversation_start()
    test_update_system_prompt()