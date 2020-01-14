# Imports go here!
# TODO: If you create a new event, remember to import it here...
from .example import ExampleEvent

# Enter the commands of your Pack here!
# TODO: and add it to the list here!
available_events = [
    ExampleEvent,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_events]
