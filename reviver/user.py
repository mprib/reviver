"""
The scope of this class currently feels a bit underwhelming, though
I suspect that this is where a bunch of the interesting stuff is going to 
happen in terms of curation of projects/history/priorities, etc

"""
import reviver.logger
import rtoml
from dataclasses import dataclass, asdict, field
from reviver.bot import Bot
from pathlib import Path
logger = reviver.logger.get(__name__)


@dataclass
class User:
    name:str
    key_location:str = None # on initial load, no key location yet
    
        
    @property
    def keys(self)->dict[str:str]:
        "load target toml file and return dictionary of keys"
        try:
            keys = rtoml.load(Path(self.key_location))

        except rtoml.TomlParsingError as e:
            logger.warn(f"keypath not valid. Error encountered of type: {type(e).__name__}")        
            logger.warn(f"Error Message: {str(e)}")
            keys = None
        
        except TypeError as e:
            logger.warn(f"keypath not valid. Error encountered of type: {type(e).__name__}")        
            logger.warn(f"Error Message: {str(e)}")
            keys = None
        
            
        return keys
    
    def set_key_location(self, key_location):
        self.key_location = str(key_location)