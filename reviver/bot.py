from dataclasses import dataclass, asdict, field

@dataclass
class Bot:
     
    name:str # must be unique among all bots in user's profile
    bot_rank:int # used for ordering bot in list
    model: str
    system_prompt:str = "you are a helpful assistant"
    max_tokens:int = 1000
    temperature:float = 1.0
    top_p: float =.5
    frequency_penalty:float =0
    presence_penalty:float =0


@dataclass
class BotGallery:
    bots: dict = field(default_factory=dict[str, Bot])