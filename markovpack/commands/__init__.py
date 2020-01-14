# Imports go here!
from .markov import MarkovCommand

# Enter the commands of your Pack here!
available_commands = [
    MarkovCommand,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_commands]
