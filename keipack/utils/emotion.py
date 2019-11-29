from enum import Enum


class Emotion(Enum):
    CAT = "cat"
    CRY = "cry"
    DISAPPOINTED = "disappointed"
    DOOTFLUTE = "dootflute"
    DOOTTRUMPET = "doottrumpet"
    GRIN = "grin"
    HALFLIFE = "halflife"
    HAPPY = "happy"
    KEY = "key"
    KEYFACE = "keyface"
    NEUTRAL = "neutral"
    QUESTION = "question"
    SMUG = "smug"
    SURPRISED = "surprised"
    WINK = "wink"
    WORRIED = "worried"
    X = "x"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.name}: {self.value}>"
