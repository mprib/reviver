from dataclasses import dataclass, field
import reviver.log

log = reviver.log.get(__name__)


@dataclass(slots=True)
class Bot:
    name: str  # must be unique among all bots in user's profile
    model: str
    rank: int  # used for ordering bot in list
    hidden: bool = False  # might not want to see a bot in your list
    system_prompt: str = "you are a helpful assistant"
    max_tokens: int = 1000
    temperature: float = 1.0
    top_p: float = 0.5
    frequency_penalty: float = 0
    presence_penalty: float = 0


@dataclass
class BotManager:
    bots: dict = field(default_factory=dict[str, Bot])

    def create_new_bot(self, name: str, model: str = None) -> bool:
        if name not in self.bots.keys():
            bot = Bot(name, model, rank=1) # new bot always at top

            # push all other bots down in rank
            for name, bt in self.bots.items():
                bt.rank += 1

            self.bots[bot.name] = bot
            log.info(f"bot added:{name}")
            return True
        else:
            log.warning(f"Bot named {name} not added...name already present")
            return False

    def get_bot(self, bot_name: str) -> Bot:
        """
        If a bot exists, then it will return that bot,
        otherwise it will create a stock bot of that name and load it in.
        This is a work around for issues where a bot is deleted
        but conversations with that bot persist.
        
        """
        if bot_name not in self.bots.keys():
            log.warn(f"{bot_name} not in bot manager... creating default bot of same name")
            self.create_new_bot(bot_name)
            
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

    def lower_rank(self, bot: Bot):
        swap_bot = self.get_bot_by_rank(bot.rank + 1)
        if swap_bot is not None:
            bot.rank, swap_bot.rank = swap_bot.rank, bot.rank
            log.info(f"Bot {bot.name} is now of rank {bot.rank}")
        else:
            log.info("No bot to swap with")

    def raise_rank(self, bot: Bot):
        swap_bot = self.get_bot_by_rank(bot.rank - 1)
        if swap_bot is not None:
            bot.rank, swap_bot.rank = swap_bot.rank, bot.rank
            log.info(f"Bot {bot.name} is now of rank {bot.rank}")
        else:
            log.info("No bot to swap with")

    def get_bot_by_rank(self, rank: int) -> Bot:
        for name, bot in self.bots.items():
            if bot.rank == rank:
                log.info(f"bot with rank {rank} is {bot.name}")
                return bot

        log.info(f"No bot of rank {rank} identified...returning None")
        return None

    def get_ranked_bots(self) -> list[Bot]:
        return sorted(list(self.bots.values()), key=lambda bot: bot.rank)

    def rename_bot(self, old_name: str, new_name: str) -> bool:
        if new_name not in self.bots.keys():
            self.bots[old_name].name = new_name
            self.bots[new_name] = self.bots.pop(old_name)

            log.info(
                f"Renaming {old_name} to {new_name}...current bots are {[bot.name for bot in self.get_ranked_bots()]}"
            )
            return True
        else:
            log.warning(f"Name already exists: {new_name}")
            return False

    def remove_bot(self, bot_name: str):
        self.bots.pop(bot_name)

    def rerank_bots(self):
        """
        If a bot has been removed, then good practice to rerank to keep indices continous
        Can also be run on load to ensure that manual copy-paste of file doesn't cause duplicate ranks floating around
        """
        rank = 1
        for bot in self.get_ranked_bots():
            bot.rank = rank
            rank += 1
