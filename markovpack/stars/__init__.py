# Imports go here!

# Enter the PageStars of your Pack here!
available_page_stars = [
]

# Enter the ExceptionStars of your Pack here!
# TODO: or to the list here if it is an ExceptionStar!
available_exception_stars = [
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in [*available_page_stars, *available_exception_stars]]
