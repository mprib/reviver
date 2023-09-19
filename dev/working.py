"""
This is a basic script where I will personally just try to use things 
as they are functioning now. I need to feel where the roadblocks are
and right now this is all just a bit too vague and conceptual....


"""
from pathlib import Path
from reviver import USER_DIR
import reviver.log
from reviver.archiver import Archive
from reviver.user import User
import rtoml

log = reviver.log.get(__name__)
log.info(f"Spinning up reviver in {USER_DIR}")

archive_dir = Path(USER_DIR, "reviver")
archive = Archive(archive_dir)
keys_toml = Path(archive_dir,"keys.toml")
user = User(name="Mac", dot_env_loc=keys_toml)
archive.store_user(user)

user = archive.get_user()

# load_keys


log.info(f"retrieving keys as {user.keys}")