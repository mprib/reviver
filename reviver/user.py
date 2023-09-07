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
log = reviver.logger.get(__name__)


@dataclass
class User:
    name:str
    key_location:str|Path = None # on initial load, no key location yet

    def __post_init__(self):
        # enforce string
        log.info("Ensuring key location stored as string.")
        self.key_location = str(self.key_location)
        
    @property
    def keys(self)->dict[str:str]:
        "load target toml file and return dictionary of keys"
        if Path(self.key_location).exists():
            try:

                keys = rtoml.load(Path(self.key_location))

            except rtoml.TomlParsingError as e:
                log.warn(f"keypath not valid. Error encountered of type: {type(e).__name__}")        
                log.warn(f"Error Message: {str(e)}")
                keys = None
            except TypeError as e:
                log.warn(f"keypath not valid. Error encountered of type: {type(e).__name__}")        
                log.warn(f"Error Message: {str(e)}")
                keys = None
                
        else:
            keys = None
        
            
        return keys
    