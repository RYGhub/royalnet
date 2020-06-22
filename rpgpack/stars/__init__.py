# Imports go here!
from .api_dnd_character import ApiDndCharacterStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiDndCharacterStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [star.__name__ for star in available_page_stars]
