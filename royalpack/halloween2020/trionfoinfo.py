import royalnet.utils as ru
from typing import *

if TYPE_CHECKING:
    from .check import Check


class TrionfoInfo:
    def __init__(self,
                 variable: str,
                 title: str,
                 roman: str,
                 name: str,
                 objective: str,
                 puzzle: str,
                 check: "Check"):
        self.variable: str = variable
        self.title: str = title
        self.roman: str = roman
        self.name: str = name
        self.objective: str = objective
        self.puzzle: str = puzzle
        self.check: "Check" = check

    def json_anonymous(self) -> ru.JSON:
        return {
            "variable": self.variable,
            "title": self.title,
            "roman": self.roman,
            "name": self.name,
            "objective": self.objective,
        }

    def json_user(self, obj) -> ru.JSON:
        status = obj.__getattribute__(self.variable)
        return {
            "variable": self.variable,
            "title": self.title,
            "roman": self.roman,
            "name": self.name,
            "objective": self.objective,
            "puzzle": self.puzzle if status is not None else None,
            "completed_on": status.timestamp() if status is not None else None
        }
