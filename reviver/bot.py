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

    def move_bot(self, old_rank: Bot, new_rank: int) -> None:
        """
        Moves a bot to a new rank and adjusts the ranks of other bots accordingly.
        """
        bot = self.get_bot_by_rank(old_rank)
        if old_rank == new_rank:
            log.info(f"No change in rank for bot {bot.name}.")
            return

        # Update ranks of other bots
        if old_rank < new_rank:
            for name, other_bot in self.bots.items():
                if old_rank < other_bot.rank <= new_rank:
                    other_bot.rank -= 1
        else:
            for name, other_bot in self.bots.items():
                if new_rank <= other_bot.rank < old_rank:
                    other_bot.rank += 1

        # Update rank of the moved bot
        bot.rank = new_rank
        log.info(f"Bot {bot.name} moved to rank {bot.rank}.")
        
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
    
    def rename_bot(self, old_name:str, new_name:str):
        self.bots[old_name].name = new_name
        self.bots[new_name]= self.bots.pop(old_name)
    
        log.info(f"Renaming bots...current bots are {[bot.name for bot in self.get_ranked_bots()]}")