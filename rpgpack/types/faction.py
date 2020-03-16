from typing import *
import enum


class Faction(enum.Enum):
    RED = "🔴"
    ORANGE = "🟠"
    YELLOW = "🟡"
    GREEN = "🟢"
    BLUE = "🔵"
    PURPLE = "🟣"
    BLACK = "⚫️"
    WHITE = "⚪️"
    BROWN = "🟤"

    @classmethod
    def get(cls, string: str):
        try:
            return cls[string.upper()]
        except KeyError:
            return cls(string)
