# Imports go here!
from .api_wiki import ApiWikiStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiWikiStar
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_page_stars]
