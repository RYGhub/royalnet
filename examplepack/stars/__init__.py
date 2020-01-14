# Imports go here!
# TODO: If you create a new star, remember to import it here...
from .api_example import ApiExampleStar
from .api_excsample import ApiExcsampleStar

# Enter the PageStars of your Pack here!
# TODO: and to add it either to the list here if it is a PageStar...
available_page_stars = [
    ApiExampleStar,
]

# Enter the ExceptionStars of your Pack here!
# TODO: or to the list here if it is an ExceptionStar!
available_exception_stars = [
    ApiExcsampleStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in [*available_page_stars, *available_exception_stars]]
