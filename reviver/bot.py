from dataclasses import dataclass, asdict, field
from enum import Enum
import reviver.log
log = reviver.log.get(__name__)



@dataclass(slots=True)
class Bot:
     
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
    bots: dict = field(default_factory=dict[str, Bot])
    
    def add_bot(self, bot:Bot):
        self.bots[bot.name] = bot
    
    def create_new_bot(self, name:str, model:str):
        """
        Bot gallery is able to track bot_ids to make sure these
        are unique
        """
        # new bots are at the top of the heap
        bot = Bot(name,model, rank=1)
        
        for name, bot in self.bots.items():
            bot.rank +=1       

        self.bots[bot.name] = bot
    
    def get_bot(self, bot_name:str)->Bot:
        
        return self.bots[bot_name]
     

    

                