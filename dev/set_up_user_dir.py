"""
Working script here to set up a folder in user directory that will hold the profiles
This is where we will have something like:

    Profile: Represents the user.
    Bot: Each bot is associated with a specific profile.
    Conversation: A conversation represents a chronological series of exchanges between a profile and a bot.

e.g.:

    Profile: Jane_Doe
        Bot: Philosophical_Phil
            Conversation: Existential_Discussion_2023_08_30
            Conversation: Metaphysical_Musings_2023_08_30
        Bot: Humorous_Holly
            Conversation: Comedy_Club_2023_08_30
"""

from reviver import USER_DIR, USER_SETTINGS, SETTING_PATH
from pathlib import Path
import rtoml
# Create a new profile folder for user

user_name = "Mac"
profile_dir = Path(USER_DIR,"Reviver", user_name )

profile_dir.mkdir(parents=True, exist_ok=True)

USER_SETTINGS["most_recent_profile_dir"] = str(profile_dir)
rtoml.dump(USER_SETTINGS, SETTING_PATH)



