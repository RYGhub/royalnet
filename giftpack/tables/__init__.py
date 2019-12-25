# Imports go here!
from .xmasgift import XmasGift

# Enter the tables of your Pack here!
available_tables = [
    XmasGift,
]

# Don't change this, it should automatically generate __all__
__all__ = [table.__name__ for table in available_tables]
