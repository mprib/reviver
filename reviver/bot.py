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
    
    def create_new_bot(self, name:str, model:str=None):
        """
        Bot gallery is able to track bot_ids to make sure these
        are unique
        """
        # new bots are at the top of the heap
        bot = Bot(name,model, rank=1)
        
        for name, bt in self.bots.items():
            bt.rank +=1       

        self.bots[bot.name] = bot
        
        log.info(f"bot added:{name}")

    def get_bot(self, bot_name:str)->Bot:
        
        return self.bots[bot_name]

    
    def lower_rank(self,bot:Bot):
        swap_bot = self.get_bot_by_rank(bot.rank+1)        
        if swap_bot is not None:
            bot.rank, swap_bot.rank = swap_bot.rank, bot.rank
            log.info(f"Bot {bot.name} is now of rank {bot.rank}")
        else:
            log.info(f"No bot to swap with") 

    def raise_rank(self,bot:Bot):
        swap_bot = self.get_bot_by_rank(bot.rank-1)        
        if swap_bot is not None:
            bot.rank, swap_bot.rank = swap_bot.rank, bot.rank
            log.info(f"Bot {bot.name} is now of rank {bot.rank}")
        else:
            log.info(f"No bot to swap with") 

    def get_bot_by_rank(self, rank:int)->Bot:
        
        for name, bot in self.bots.items():
            if bot.rank==rank:
                log.info(f"bot with rank {rank} is {bot.name}")
                return bot
        
        log.info(f"No bot of rank {rank} identified...returning None")
        return None
    

    def get_ranked_bots(self)->list[Bot]:
        return sorted(list(self.bots.values()), key=lambda bot:bot.rank)
        