from enum import Enum, auto


class Emotion(Enum):
    HAPPY = auto()
    SAD = auto()
    ANGRY = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.name}: {self.value}>"
