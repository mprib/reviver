import reviver.logger

logger = reviver.logger.get(__name__)
from reviver.conversation import Message, Conversation


def test_conversation():
    msg1 = Message(role="user", content="This is a test")
    msg2 = Message(role="assistant", content="I'm just here to help.")

    convo = Conversation()

    convo.add_message(msg1)
    convo.add_message(msg2)

    logger.info(f"conversation list is {convo.prompt}")
    target_list = [
        {"role": "user", "content": "This is a test"},
        {"role": "assistant", "content": "I'm just here to help."},
    ]
    assert convo.prompt == target_list

def test_token_size():
    msg1 = Message(role="user", content="This is a test")
    msg2 = Message(role="assistant", content="This is a test")

    logger.info(f"test message size is {msg1.token_size}")
    assert(msg1.token_size == msg2.token_size)
    
    
    convo = Conversation()

    convo.add_message(msg1)
    convo.add_message(msg2)

    assert(convo.token_size == msg1.token_size+msg2.token_size)
    logger.info(f"conversation size is {convo.token_size}")


if __name__ == "__main__":
    test_conversation()
    test_token_size()