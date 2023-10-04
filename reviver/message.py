from reviver import ROOT
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
import reviver.log

log = reviver.log.get(__name__)


@dataclass(
    slots=True, frozen=False
)  # not frozen because content of message is built up iteratively
class Message:
    """
    The bulk of this class is dedicated to processing the core data to be formatted appropriately in the webview widget
    """

    role: str
    content: str
    time: str = None

    def __post_init__(self):
        if self.time is None:
            self.time = datetime.now()

    @property
    def _id(self):
        """
        Used to identify specific message divisions in conversation widget's webview html
        """
        _id = f"message-{self.time}"
        return _id

    @property
    def token_size(self):
        """
        Token size is a generalization based on the rule that 1 token ~= 4 characters:
        https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        """
        return len(self.content) / 4

    @property
    def time_as_datetime(self):
        format = "%Y-%m-%d %H:%M:%S.%f"
        t = datetime.strptime(self.time, format)
        return t




