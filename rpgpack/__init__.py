# This is a template Pack __init__. You can use this without changing anything in other packages too!

from . import commands, tables, stars, version
from .commands import available_commands
from .tables import available_tables
from .stars import available_page_stars, available_exception_stars

__all__ = [
    "commands",
    "tables",
    "stars",
    "version",
    "available_commands",
    "available_tables",
    "available_page_stars",
    "available_exception_stars",
]
