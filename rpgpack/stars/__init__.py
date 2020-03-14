# Imports go here!
from .api_dnd_character_get import ApiDndCharacterGetStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiDndCharacterGetStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [star.__name__ for star in available_page_stars]
