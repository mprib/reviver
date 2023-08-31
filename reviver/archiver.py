import rtoml
import reviver.logger
from dataclasses import dataclass, asdict

logger = reviver.logger.get(__name__)
from pathlib import Path
from reviver.conversation import Conversation, Message
from reviver.bot import Bot
from reviver.user import User

class Archiver:
    def __init__(self, user_dir: Path) -> None:
        self.profile_dir = user_dir
        self.user_toml = Path(self.profile_dir, "user.toml")

        #make sure that there is a place to store data
        if not self.user_toml.parent.exists():
            self.user_toml.parent.mkdir(parents=True, exist_ok=True)
        
    def store_conversation(self, convo: Conversation) -> None:
        self.store_user(convo.user)
        
        toml_data = {}
        toml_data["bot"] = asdict(convo.bot)
        
        messages = get_messages_for_toml(convo)
        toml_data["messages"] = messages
        logger.info(messages)

        # conversations are stored under bot subfolder

        target_dir = Path(self.profile_dir, convo.bot.name)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = Path(target_dir, f"{convo.title}.toml")

        with open(target_path, "w") as f:
            rtoml.dump(toml_data, f)

    def store_user(self,user:User)-> None:
        with open(self.user_toml, "w") as f:
            
            # preliminary data will have bots as dictionary of Bot
            preliminary_data = asdict(user)

            for key, value in preliminary_data.items():
                if 
            
            rtoml.dump(asdict(user), self.user_toml)

    def get_user(self)->User:
        
        user_data = rtoml.load(self.user_toml)
        user = User(**user_data)
        return user

    def save_bot(self, bot:Bot)->None:
        
        pass 
        
    def get_bot(self, bot_name: str) -> Bot:

        user_data = rtoml.load(self.user_toml)
        bots_data = user_data["bots"]

        for bot_data in bots_data:
            if bot_data["name"] == bot_name:
                return Bot(**bot_data)

        return bot_data


    def get_messages(self, bot: Bot, title: str) -> dict[int:Message]:
        target_dir = Path(self.profile_dir, bot.name)
        target_path = Path(target_dir, f"{title}.toml")

        # note that messages are in a table, therefore are a list of dictionaries with identical layouts

        toml_data = rtoml.load(target_path)
        messages = {}
        for msg in toml_data["messages"]:
            role = msg["role"]
            content = msg["content"]
            time = msg["time"]
            index = msg["index"]

            messages[index] = Message(role, content, time)

        logger.info(f"Messages loaded")
        return messages

    def get_conversation(self, bot: Bot, title: str) -> Conversation:
        messages = self.get_messages(bot, title)
        message_count = len(messages.keys())
        user = self.get_user()
        convo = Conversation(user, bot, messages, message_count)
        return convo


def get_messages_for_toml(convo: Conversation):
    messages = []
    logger.info(convo.messages_prompt)
    for index, msg in convo.messages.items():
        msg_data = asdict(msg)
        msg_data["index"] = index
        messages.append(msg_data)

    return messages
