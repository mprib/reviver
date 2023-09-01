from dataclasses import dataclass, asdict, field
from enum import Enum






@dataclass
class Bot:
     
    bot_id:int  
    name:str # must be unique among all bots in user's profile
    model: str 
    rank:int # used for ordering bot in list
    hidden:bool = False # might not want to see a bot in your list
    system_prompt:str = "you are a helpful assistant"
    max_tokens:int = 1000
    temperature:float = 1.0
    top_p: float =.5
    frequency_penalty:float =0
    presence_penalty:float =0


@dataclass
class BotGallery:
    bots: dict = field(default_factory=dict[int, Bot])
    
    def add_bot(self, bot:Bot):
        self.bots[bot.bot_id] = bot
    
    def create_new_bot(self, name:str, model:str):
        """
        Bot gallery is able to track bot_ids to make sure these
        are unique
        """
        bot_id = self.get_max_id()+1

        # new bots are at the top of the heap
        bot = Bot(bot_id,name,model, rank=1)
        self.bots[bot_id] = bot
    
     
     
    def get_max_id(self):
        bot_ids = []
        for bot_id, bot in self.bots.items():
            bot_ids.append(bot_id)

        if len(bot_ids)==0:
            max_id = 0
        else:
            max_id = max(bot_ids)
        return max_id

    

                