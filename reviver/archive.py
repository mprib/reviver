import reviver.log
from dataclasses import asdict
from pathlib import Path
from reviver.conversation import Conversation, Message
from reviver.bot import Bot, BotGallery
import rtoml


log = reviver.log.get(__name__)


class Archive:
    """
    Aims for simplicity in implementation/auditing/tweaking by storing all data in toml files
    """
    def __init__(self, reviver_data_dir: Path) -> None:
        self.reviver_dir = reviver_data_dir
        self.bots_dir = Path(self.reviver_dir, "bots")
        self.conversations_dir = Path(self.reviver_dir, "conversations")

        # check that appropriate directories exist
        self.bots_dir.mkdir(parents=True, exist_ok=True)
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        
    def bot_path(self, bot_name:str)->Path:
        return Path(self.bots_dir, str(bot_name)+".toml")
     
    def store_bot(self, bot: Bot) -> None:
        bot_data = asdict(bot)
        log.info(f"Storing... {bot.name}")
        with open(self.bot_path(bot.name), "w+") as f:
            rtoml.dump(bot_data,f)    


    def store_bot_gallery(self, bot_gallery:BotGallery):
        for bot_id, bot in bot_gallery.bots.items():
            self.store_bot(bot)
            
    
        
    def load_bot_gallery(self):
        bots = {}
        for bot_toml in Path(self.reviver_dir, "bots").iterdir():
            bot_name = bot_toml.stem
            bot = self.get_bot(bot_name)
            bots[bot_name] = bot
        
        bot_gallery = BotGallery(bots)
        return bot_gallery
         
        
    def get_bot(self, bot_name:str) -> Bot:
        bot_data = rtoml.load(self.bot_path(bot_name))
        bot = Bot(**bot_data)
        return bot


    def store_conversation(self, convo: Conversation) -> None:
        """
        Note: this will store the messages and id of the bot that participated
        in the conversation, but it won't save the bot data itself
        """

        log.info(f"Storing conversation {convo.title}")
        convo_data = {}
        convo_data["title"] = convo.title
        convo_data["bot_name"] = convo.bot.name

        messages = {str(position):asdict(msg) for position,msg in convo.messages.items()}
        convo_data["messages"] = messages

        # Determine the path to the file where the conversation will be stored
        convo_path = Path(self.conversations_dir, f"{convo.title}.toml")

        # Write the dictionary to a toml file
        with open(convo_path, "w") as f:
            rtoml.dump(convo_data, f)

    def load_conversation(self, convo_title: str, bot_gallery: BotGallery) -> Conversation:
        """
        Loads a conversation from a toml file.
        Requires a BotGallery to find the right bot.
        """

        log.info(f"Loading conversation {convo_title}")
        # Determine the path to the file where the conversation is stored
        convo_path = Path(self.conversations_dir, f"{convo_title}.toml")

        # Read the dictionary from the toml file
        with open(convo_path, "r") as f:
            convo_data = rtoml.load(f)

        # Fetch the bot from BotGallery
        bot = bot_gallery.get_bot(convo_data["bot_name"])

        messages = {}

        # Transform the dict back to Message objects
        for position, msg_data in convo_data["messages"].items():
            msg = Message(**msg_data)
            messages[int(position)] = msg

        # Create a Conversation object with loaded data
        convo = Conversation(
            bot = bot,
            title = convo_data["title"],
            messages = messages
        )

        return convo 
         
