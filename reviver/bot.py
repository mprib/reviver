from dataclasses import dataclass, asdict

@dataclass
class Bot:
    
    name:str # must be unique among all bots in user's profile
    model: str
    system_prompt:str = "you are a helpful assistant"
    max_tokens:int = 1000
    temperature:float = 1.0
    top_p: float =.5
    frequency_penalty:float =0
    presence_penalty:float =0

