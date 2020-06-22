# Imports go here!
from .wikipage import WikiPage
from .wikirevision import WikiRevision
from .wikideletion import WikiDeletion

# Enter the tables of your Pack here!
available_tables = [
    WikiPage,
    WikiRevision,
    WikiDeletion,
]

# Don't change this, it should automatically generate __all__
__all__ = [table.__name__ for table in available_tables]
