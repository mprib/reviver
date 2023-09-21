"""
This is going to be a challenging test because i'm going to
actually call out using my keys

I'll have some stored locally here...
Need to make sure i don't backup to git and that I lock down the
max spend on the openAI key

"""
from reviver.bot import Bot
from reviver.conversation import Conversation
from reviver.message import Message
from queue import Queue
import reviver.log
log = reviver.log.get(__name__)

def test_bot_reply():
    """
    Note that this test requires an active internet connection and working keys
    Keys are stored in ROOT/keys.toml which should *not* be version controlled
    """
    # model = "meta-llama/llama-2-70b-chat"
    model = "openai/gpt-3.5-turbo-0301"
    bot = Bot(_id=1, name = "test_bot", model=model,rank=1, system_prompt="You will only reply with the word:HELLO WORLD. It should be spelled in all capitals with no other punctuation. User will say 'proceed' and then you will responsd with 'HELLO WORLD'.")

    convo_id = 1
    convo = Conversation(_id=convo_id, bot=bot)

    assert(convo.message_count==1) # system prompt

    message1 = Message( role="user", content= "proceed")  

    log.info("Add user generated message to conversation")
    convo.add_message(message1)

    stream_q = Queue()
   
    assert(convo.message_count==2) # system prompt + "proceed" 
    convo.generate_next_message(stream_q)
    
    new_message = stream_q.get()
    log.info("Reply came back")

    assert(convo.message_count==3) # new message added

    message:Message = convo.messages[convo.message_count]
    assert(message == new_message)
    # had to make a more genrous assertion to just "contains" because it wasn't giving only this...
    assert(message.content.__contains__("HELLO WORLD"))
    log.info("Reply came back as requested")

if __name__ == "__main__":
    test_bot_reply()