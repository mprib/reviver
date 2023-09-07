"""
The session will hold the primary objects that the GUI interact with. When provided with an data directory
"""
from pathlib import Path
from reviver.archiver import Archive

class Session:
    
    def __init__(self, reviver_data_dir:Path) -> None:
        self.data_dir = reviver_data_dir
        self.archive = Archive(self.data_dir)

    