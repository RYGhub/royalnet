# Imports go here!
# TODO: If you create a new command, remember to import it here...
from .example import ExampleCommand

# Enter the commands of your Pack here!
# TODO: and add it to the list here!
available_commands = [
    ExampleCommand,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_commands]
