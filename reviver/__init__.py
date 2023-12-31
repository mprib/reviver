import os
from pathlib import Path
import rtoml

application_name = "reviver"

if os.name == 'nt':   
    app_dir = os.getenv('LOCALAPPDATA')
else:  
    app_dir = os.path.join(os.path.expanduser("~"), '.local', 'share')

APP_DIR = Path(app_dir,application_name )
APP_DIR.mkdir(exist_ok=True, parents=True)

# Create a toml file for storing things like where to look for most recent project
SETTING_PATH = Path(APP_DIR, 'settings.toml')
# user's home directory could be helpful for initial choice of where to save
USER_DIR = Path(os.path.expanduser("~"))
ROOT = Path(__file__).parent.parent


if SETTING_PATH.exists():
    REVIVER_SETTINGS = rtoml.load(SETTING_PATH)
else:
    REVIVER_SETTINGS = {"recent_archives":[]} 

LOG_PATH = Path(APP_DIR, "log.txt")
