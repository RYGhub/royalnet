# Imports go here!
from .dndactivecharacters import DndActiveCharacter
from .dndcharacters import DndCharacter
from .dndbattle import DndBattle
from .dndbattleunit import DndBattleUnit
from .dndactivebattle import DndActiveBattle

# Enter the tables of your Pack here!
available_tables = [
    DndActiveCharacter,
    DndCharacter,
    DndBattle,
    DndBattleUnit,
    DndActiveBattle,
]

# Don't change this, it should automatically generate __all__
__all__ = [table.__name__ for table in available_tables]
