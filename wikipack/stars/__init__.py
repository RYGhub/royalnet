# Imports go here!
from .api_wiki import ApiWikiStar
from .api_wiki_list import ApiWikiListStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiWikiStar,
    ApiWikiListStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_page_stars]
