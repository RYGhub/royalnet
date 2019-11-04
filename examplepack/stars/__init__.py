# Imports go here!
# TODO: If you create a new star, remember to import it here...
# from .example import ExampleStar
# from .api_example import ApiExampleStar

# Enter the PageStars of your Pack here!
# TODO: and to add it either to the list here if it is a PageStar...
available_page_stars = [
    # ExampleStar,
    # ApiExampleStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_page_stars]
