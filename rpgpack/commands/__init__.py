# Imports go here!
from .roll import RollCommand
from .dice import DiceCommand
from .dndactive import DndactiveCommand
from .dndinfo import DndinfoCommand
from .dndnew import DndnewCommand
from .dndedit import DndeditCommand
from .dndroll import DndrollCommand
from .dnditem import DnditemCommand
from .dndspell import DndspellCommand
from .testhealth import TesthealthCommand
from .testfaction import TestfactionCommand
from .dndnewbattle import DndnewbattleCommand
from .dndactivebattle import DndactivebattleCommand
from .dndaddunit import DndaddunitCommand
from .dnddamage import DnddamageCommand
from .dndheal import DndhealCommand
from .dndstatus import DndstatusCommand
from .dndextra import DndextraCommand
from .dnddeathsave import DnddeathsaveCommand
from .dndjoinbattle import DndjoinbattleCommand

# Enter the commands of your Pack here!
available_commands = [
    RollCommand,
    DiceCommand,
    DndactiveCommand,
    DndinfoCommand,
    DndnewCommand,
    DndeditCommand,
    DndrollCommand,
    DnditemCommand,
    DndspellCommand,
    TesthealthCommand,
    TestfactionCommand,
    DndnewbattleCommand,
    DndactivebattleCommand,
    DndaddunitCommand,
    DnddamageCommand,
    DndhealCommand,
    DndstatusCommand,
    DndextraCommand,
    DnddeathsaveCommand,
    DndjoinbattleCommand,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_commands]
