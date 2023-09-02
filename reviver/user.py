"""
The scope of this class currently feels a bit underwhelming, though
I suspect that this is where a bunch of the interesting stuff is going to 
happen in terms of curation of projects/history/priorities, etc

"""
import reviver.logger
logger = reviver.logger.get(__name__)
from dataclasses import dataclass, asdict, field
from reviver.bot import Bot


@dataclass
class User:
    name:str
    key_location:str = None # on initial load, no key location yet
    
        
    