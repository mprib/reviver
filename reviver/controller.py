"""
The session will hold the primary objects that the GUI interact with. When provided with an data directory
"""
from PySide6.QtCore import QObject, Signal
from pathlib import Path
from dataclasses import asdict
from reviver.archive import Archive
import reviver.log

from reviver.bot import Bot, BotGallery
from reviver.conversation import Conversation
from dotenv import load_dotenv
from os import getenv
from reviver.models_data import ModelSpecSheet
from datetime import datetime
from reviver.gui.html_styler import style_conversation, style_message

log = reviver.log.get(__name__)


class Controller(QObject):
    """
    A simple facade to the back end object management that will be the
    single point of contact for all GUI elements.
    """

    conversation_updated = Signal()
    message_added = Signal(str, str, str)
    message_updated = Signal(str, str, str)
    message_complete = Signal()

    def __init__(self, data_directory: Path) -> None:
        super().__init__()
        log.info(f"Launching session for data stored in {data_directory}")
        self.data_directory = data_directory

        # load archive if it exists; otherwise creates it
        self.archive = Archive(self.data_directory)

        self.conversations = {}
        self.active_conversation = None

        self.bot_gallery = self.archive.get_bot_gallery()

        # load API key if it's available and use it to set the spec sheet
        try:
            env_location = Path(self.data_directory, ".env")
            load_dotenv(dotenv_path=env_location)
            self.key = getenv("OPEN_ROUTER_API_KEY")
            self.update_spec_sheet()
        except:
            pass

        self.connect_signals()
        
    def connect_signals(self):
        self.message_complete.connect(self.store_active_conversation)
        self.message_added.connect(self.store_active_conversation)


    def add_bot(self, bot_name: str) -> bool:
        """
        boolean return communicates if add was successful
        """
        success = self.bot_gallery.create_new_bot(bot_name)
        self.archive.store_bot_gallery(self.bot_gallery)
        return success

    def remove_bot(self, bot_name: str):
        self.bot_gallery.remove_bot(bot_name)
        self.bot_gallery.rerank_bots()
        self.archive.remove_bot(bot_name)

    def rename_bot(self, old_name, new_name) -> bool:
        success = self.bot_gallery.rename_bot(old_name, new_name)
        if success:
            bot = self.bot_gallery.get_bot(new_name)
            # note: important to rename bot archive prior to storing it...
            self.archive.rename_bot(old_name, new_name)
            self.archive.store_bot(bot)

        return success

    def get_ranked_bot_names(self):
        log.info("Getting bots by rank")
        return [bot.name for bot in self.bot_gallery.get_ranked_bots()]

    def update_spec_sheet(self):
        self.spec_sheet = ModelSpecSheet(self.key)

    def get_spec_sheet(self) -> ModelSpecSheet:
        return self.spec_sheet

    def get_bot_data(self, bot_name: str) -> dict:
        """
        passes dictionary of bot properties to GUI...does not expose bot to GUI
        """
        if bot_name in self.bot_gallery.bots.keys():
            bot = self.bot_gallery.bots[bot_name]
            return asdict(bot)
        else:
            return None

    def update_bot(self, bot_name: str, **kwargs):
        """
        Updates the bot given the name and the properties to update.
        """
        if bot_name in self.bot_gallery.bots.keys():
            bot = self.bot_gallery.bots[bot_name]

            for key, value in kwargs.items():
                if hasattr(bot, key):
                    setattr(bot, key, value)
                else:
                    log.warning(f"Bot does not have property {key}")

            self.archive.store_bot(bot)
        else:
            log.warning(f"No bot by name of {bot_name}")


    def move_bot(self, old_rank, new_rank):
        self.bot_gallery.move_bot(old_rank, new_rank)
        self.archive.store_bot_gallery(self.bot_gallery)

    def start_conversation(self, bot_name: str):
        """ """
        bot = self.bot_gallery.get_bot(bot_name)

        convo_title = str(datetime.now())
        for char in [":", " ", ".", "-"]:
            convo_title = convo_title.replace(char, "")

        convo = Conversation(bot=bot, title=convo_title)
        self.conversations[convo_title] = convo
        self.active_conversation = convo
        self.archive.store_conversation(convo)

    def store_active_conversation(self):
        self.archive.store_conversation(self.active_conversation)
        
    def get_active_conversation_html(self):
        if self.active_conversation is not None:
            return style_conversation(self.active_conversation)
        else:
            return None

    def rename_conversation(self, old_title, new_title):
        pass

    def add_new_user_message(self, content: str):
        self.active_conversation.add_user_message(content, self.message_added)
        self.active_conversation.generate_reply(
            message_added=self.message_added,
            message_updated=self.message_updated,
            message_complete=self.message_complete,
        )
        