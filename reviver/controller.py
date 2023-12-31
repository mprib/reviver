"""
The session will hold the primary objects that the GUI interact with. When provided with an data directory
"""
from PySide6.QtCore import QObject, Signal
from pathlib import Path
from dataclasses import asdict
from reviver.archive import Archive
import reviver.log

from reviver.bot import Bot, BotManager
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
    refresh_active_conversation = Signal()
    new_active_conversation = Signal()
    bot_updated = Signal()
    bot_renamed = Signal()
    bot_added = Signal()
    bots_reordered = Signal()


    def __init__(self, data_directory: Path) -> None:
        super().__init__()
        log.info(f"Launching session for data stored in {data_directory}")
        self.data_directory = data_directory

        # load archive if it exists; otherwise creates it
        self.archive = Archive(self.data_directory)
        self.bot_manager = self.archive.get_bot_manager()
        self.convo_manager = self.archive.get_conversation_manager(self.bot_manager)

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
        """
        I suspect that this is a poor use of the Signaling mechanism
        This is something that needs to be changes, likely using Queues to 
        communicate between the model and controller and then signals to communicate
        between the controller and the view        
        """

        self.message_complete.connect(self.store_active_conversation)
        self.message_added.connect(self.store_active_conversation)

    def set_active_convo_bot(self, bot_name):
        if bot_name:
            log.info(f"Setting active bot to {bot_name}")
            # self.active_bot_name = bot_name
            bot = self.bot_manager.get_bot(bot_name)
            # if self.convo_manager.active_conversation is not None:
            self.convo_manager.active_conversation.bot = bot
            self.set_selected_bot(bot_name)
        
            # pass in message added signal
            self.convo_manager.active_conversation.update_system_prompt() 
            self.refresh_active_conversation.emit()
            log.info(f"Signalling bots updated after setting active bot to {bot_name}")
            self.bot_updated.emit()
            self.store_active_conversation()

    def add_bot(self, bot_name: str) -> bool:
        """
        boolean return communicates if add was successful
        """
        success = self.bot_manager.create_new_bot(bot_name)
        log.info(f"About to signal update of bots after creating new bot: {bot_name}")
        self.bot_added.emit()
        self.archive.store_bot_manager(self.bot_manager)
        return success

    def remove_bot(self, bot_name: str):
        """
        Note that this does not currently address issues with the conversation having a deleted bot
        """
        self.bot_manager.remove_bot(bot_name)
        self.bot_manager.rerank_bots()
        self.bot_manager.selected_bot = self.bot_manager.get_bot_by_rank(1)
        self.archive.remove_bot(bot_name)

    def rename_bot(self, old_name, new_name) -> bool:
        success = self.bot_manager.rename_bot(old_name, new_name)
        if success:
            bot = self.bot_manager.get_bot(new_name)
            # note: important to rename bot archive prior to storing it...
            self.archive.rename_bot(old_name, new_name)
            log.info(f"Updating {old_name} to {new_name} and signalling bots updated.")
            self.bot_renamed.emit()
            self.archive.store_bot(bot)
            
        return success

    def get_bot_data(self, bot_name: str) -> dict:
        """
        passes dictionary of bot properties to GUI...does not expose bot to GUI
        """
        if bot_name in self.bot_manager.bots.keys():
            bot = self.bot_manager.bots[bot_name]
            return asdict(bot)
        else:
            return None

    def set_selected_bot(self,bot_name):
        bot = self.bot_manager.get_bot(bot_name)
        self.bot_manager.selected_bot = bot
        
    def get_selected_bot_name(self):
        """
        If not bots yet, then this will be None
        """
        return self.bot_manager.selected_bot.name

    def update_bot(self, bot_name: str, **kwargs):
        """
        Updates the bot given the name and the properties to update.
        Note that current implementation uses kwargs (might be a mistake)
        All arguments (other than bot_name) must be passed in with argument name
        """
        if bot_name in self.bot_manager.bots.keys():
            bot = self.bot_manager.bots[bot_name]

            for key, value in kwargs.items():
                if hasattr(bot, key):
                    setattr(bot, key, value)
                else:
                    log.warning(f"Bot does not have property {key}")

            # system prompt may have changed
            if self.convo_manager.active_conversation is not None:
                self.convo_manager.active_conversation.update_system_prompt() 

            self.bot_updated.emit()
            self.archive.store_bot(bot)
        else:
            log.warning(f"No bot by name of {bot_name}")


    def move_bot(self, old_rank, new_rank):
        self.bot_manager.move_bot(old_rank, new_rank)
        self.archive.store_bot_manager(self.bot_manager)
        self.bots_reordered.emit()

    def get_ranked_bot_names(self):
        log.info("Getting bots by rank")
        return [bot.name for bot in self.bot_manager.get_ranked_bots()]

    def update_spec_sheet(self):
        self.spec_sheet = ModelSpecSheet(self.key)

    def get_spec_sheet(self) -> ModelSpecSheet:
        return self.spec_sheet


    def start_conversation(self, bot_name: str):
        """ """
        bot = self.bot_manager.get_bot(bot_name)
        # self.active_bot_name = bot_name
        self.convo_manager.new_active_conversation(bot)
        self.archive.store_conversation(self.convo_manager.active_conversation)
        self.new_active_conversation.emit()

    def store_active_conversation(self):
        self.archive.store_conversation(self.convo_manager.active_conversation)
    
    def get_active_bot_name(self):
        if self.convo_manager.active_conversation is not None:
            return self.convo_manager.active_conversation.bot.name
        else:
            return None
     
    def get_active_conversation_html(self):
        if self.convo_manager.active_conversation is not None:
            return style_conversation(self.convo_manager.active_conversation)
        else:
            return "Create new conversation to begin"

    def set_active_conversation(self, conversation_title:str):
        self.convo_manager.set_active_conversation(conversation_title)
        self.new_active_conversation.emit()


    def get_active_conversation_title(self):
        title = None
        if self.convo_manager.active_conversation is not None:
            title = self.convo_manager.active_conversation.title
        return title
     
    def rename_conversation(self, old_title, new_title):
        pass

    def add_new_user_message(self, content: str):
        self.convo_manager.active_conversation.add_user_message(content, self.message_added)
        self.convo_manager.active_conversation.generate_reply(
            message_added=self.message_added,
            message_updated=self.message_updated,
            message_complete=self.message_complete,
        )
        

    def get_conversation_list(self):
        return self.convo_manager.get_conversation_list()