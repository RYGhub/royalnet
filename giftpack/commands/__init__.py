# Imports go here!
from .addgift import AddgiftCommand
from .delgift import DelgiftCommand
from .getgift import GetgiftCommand
from .getgiftdst import GetgiftdstCommand
from .getgiftid import GetgiftidCommand
from .getgiftsrc import GetgiftsrcCommand
from .listgifts import ListgiftsCommand

# Enter the commands of your Pack here!
available_commands = [
    AddgiftCommand,
    DelgiftCommand,
    GetgiftCommand,
    GetgiftdstCommand,
    GetgiftidCommand,
    GetgiftsrcCommand,
    ListgiftsCommand,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_commands]
