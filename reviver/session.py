"""
The session will hold the primary objects that the GUI interact with. When provided with an data directory
"""
from pathlib import Path
from reviver.archiver import Archive
import reviver.log
from reviver.bot import Bot, BotGallery
log = reviver.log.get(__name__)

class Session:
    
    def __init__(self, reviver_data_dir:Path) -> None:

        log.info(f"Launching session for data stored in {reviver_data_dir}")
        self.archive_dir = reviver_data_dir
        self.archive = Archive(self.archive_dir)
        self.user = self.archive.get_user()

        self.active_conversations = {}
        self.bot_gallery = self.archive.get_bot_gallery()


    def create_new_conversation(self, bot_id:int):
        bot = self.archive.get_bot(bot_id)
        