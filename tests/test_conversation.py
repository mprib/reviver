import reviver.log

logger = reviver.log.get(__name__)
from reviver.conversation import Message, Conversation
from reviver.bot import Bot
from reviver.user import User

def test_conversation_creation():

    msg1 = Message(conversation_id=1, position = 1, role="user", content="This is a test")
    msg2 = Message(conversation_id=1, position = 2, role="assistant", content="sup?")
    
    bot = Bot(_id = 1, name="test_bot", model = "llama_70b", rank=1, system_prompt="good bot")
    user = User(name = "Test User")
    convo = Conversation(_id=1, title = "New conversation", user=user, bot=bot)

    convo.add_message(msg1)
    convo.add_message(msg2)

    logger.info(f"conversation list is {convo.messages_prompt}")
    target_list = [
        {"role": "system", "content": "good bot"},
        {"role": "user", "content": "This is a test"},
        {"role": "assistant", "content": "sup?"},
    ]
    assert convo.messages_prompt == target_list

def test_token_size():
    msg1 = Message(conversation_id=1, position = 1, role="user", content="This is a test")
    msg2 = Message(conversation_id=1, position = 2, role="assistant", content="This is a test")

    logger.info(f"test message size is {msg1.token_size}")
    assert(msg1.token_size == msg2.token_size)
    
    bot = Bot(_id = 1, name="test_bot", model = "llama_70b", rank = 1, system_prompt="good bot")
    user = User(name = "Test User")
    convo = Conversation(_id=1, title = "New conversation",user=user, bot=bot)
    

    system_message = convo.messages[0]
    convo.add_message(msg1)
    convo.add_message(msg2)


    # three messages are in the conversation now, including the system prompt
    assert(convo.token_size == msg1.token_size+msg2.token_size + system_message.token_size)
    logger.info(f"conversation size is {convo.token_size}")


if __name__ == "__main__":
    test_conversation_creation()
    test_token_size()