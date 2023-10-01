"""
The session will hold the primary objects that the GUI interact with. When provided with an data directory
"""
from pathlib import Path
from dataclasses import asdict
from reviver.archive import Archive
import reviver.log

from reviver.bot import Bot, BotGallery
from dotenv import load_dotenv
from os import getenv
from reviver.models_data import ModelSpecSheet

log = reviver.log.get(__name__)

class Controller:
    """
    A simple facade to the back end object management that will be the
    single point of contact for all GUI elements. 
    """ 
    def __init__(self, reviver_data_dir:Path) -> None:

        log.info(f"Launching session for data stored in {reviver_data_dir}")
        self.archive_dir = reviver_data_dir
        
        # load archive if it exists; otherwise creates it
        self.archive = Archive(self.archive_dir)

        self.active_conversations = {}
        self.bot_gallery = self.archive.load_bot_gallery()

        # load API key if it's available and use it to set the spec sheet
        try:
            env_location = Path(self.archive_dir,".env")
            load_dotenv(dotenv_path=env_location)
            self.key = getenv("OPEN_ROUTER_API_KEY")
            self.update_spec_sheet()
        except:
            pass
        
    def add_bot(self, bot_name:str)->bool:
        """
        boolean return communicates if add was successful
        """
        success = self.bot_gallery.create_new_bot(bot_name)
        self.archive.store_bot_gallery(self.bot_gallery)
        return success
    
    def rename_bot(self, old_name, new_name)->bool:
        success = self.bot_gallery.rename_bot(old_name,new_name)
        if success:
            bot = self.bot_gallery.get_bot(new_name)
            # note: important to rename bot archive prior to storing it...
            self.archive.rename_bot(old_name,new_name)        
            self.archive.store_bot(bot)

        return success
     
    def get_ranked_bots(self):
        log.info("Getting bots by rank")
        return self.bot_gallery.get_ranked_bots()
            
    def update_spec_sheet(self):
        self.spec_sheet = ModelSpecSheet(self.key)

    def get_spec_sheet(self)->ModelSpecSheet:
        return self.spec_sheet
    
    def get_bot_data(self, bot_name:str)->dict:
        """
        passes dictionary of bot properties to GUI...does not expose bot to GUI
        """
        if bot_name in self.bot_gallery.bots.keys():
            bot = self.bot_gallery.bots[bot_name]
            return asdict(bot)
        else:
            return None
    
    def update_bot(self,
                   name:str,
                   model:str,
                   system_prompt:str,
                   max_tokens:int,
                   temperature:float,
                   top_p:int,
                   frequency_penalty:float,
                   presence_penalty:float
        ):
        
        if name in self.bot_gallery.bots.keys(): 
            bot = self.bot_gallery.bots[name]
            bot.model=model
            bot.system_prompt=system_prompt
            bot.max_tokens=max_tokens
            bot.temperature=temperature
            bot.top_p=top_p
            bot.frequency_penalty=frequency_penalty
            bot.presence_penalty=presence_penalty

            self.archive.store_bot(bot)
        else:
            log.warning(f"No bot by name of {name}")
            
    def move_bot(self, old_rank, new_rank):
        self.bot_gallery.move_bot(old_rank, new_rank)
        self.archive.store_bot_gallery(self.bot_gallery)