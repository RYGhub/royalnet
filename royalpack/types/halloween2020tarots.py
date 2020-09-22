from typing import *


class Halloween2020Tarot:
    def __init__(self,
                 variable: str,
                 title: str,
                 roman: str,
                 name: str,
                 objective: str,
                 puzzle: str,
                 check: Optional[Callable[..., Awaitable[...]]]):
        self.variable: str = variable
        self.title: str = title
        self.roman: str = roman
        self.name: str = name
        self.objective: str = objective
        self.puzzle: str = puzzle
        self.check: Optional[Callable[..., Awaitable[...]]] = check


halloween2020tarots = (
    Halloween2020Tarot(
        variable="zero",
        title="o",
        roman="0",
        name="Il Folle",
        objective="Partecipa ai Trionfi Reali.",
        puzzle="Scopri nuovi indizi ottenendo dei Trionfi!",
        check=None,
    ),
    Halloween2020Tarot(
        variable="i",
        title="i",
        roman="I",
        name="Il Mago",
        objective="Trova una magia che possa fare almeno 250 danni.",
        puzzle="L'ultimo giorno del decimo mese...",
        check=None,
    ),
    Halloween2020Tarot(
        variable="ii",
        title="ii",
        roman="II",
        name="La Papessa",
    ),
    Halloween2020Tarot(
        variable="iii",
        title="iii",
        roman="III",
        name="L'Imperatrice",
    ),
    Halloween2020Tarot(
        variable="iv",
        title="iv",
        roman="IV",
        name="L'Imperatore",
    ),
    Halloween2020Tarot(
        variable="v",
        title="v",
        roman="V",
        name="Il Papa",
    ),
    Halloween2020Tarot(
        variable="vi",
        title="vi",
        roman="VI",
        name="Gli Amanti",
        objective="Completa [url=https://store.steampowered.com/app/698780]Doki Doki "
                  "Literature Club[/url].",
    ),
    Halloween2020Tarot(
        variable="vii",
        title="vii",
        roman="VII",
        name="Il Carro",
    ),
    Halloween2020Tarot(
        variable="viii",
        title="viii",
        roman="VIII",
        name="La Giustizia",
    ),
    Halloween2020Tarot(
        variable="ix",
        title="ix",
        roman="IX",
        name="L'Eremita",
    ),
    Halloween2020Tarot(
        variable="x",
        title="x",
        roman="X",
        name="La Fortuna",
    ),
    Halloween2020Tarot(
        variable="xi",
        title="xi",
        roman="XI",
        name="La Forza",
        objective="Gioca 3 partite Ranked 1v1 su "
                  "[url=https://steamcommunity.com/id/steffo1999/stats/appid/291550/achievements]Brawlhalla[/url]."
    ),
    Halloween2020Tarot(
        variable="xii",
        title="xii",
        roman="XII",
        name="L'Appeso",
    ),
    Halloween2020Tarot(
        variable="xiii",
        title="xiii",
        roman="XIII",
        name="La Morte",
    ),
    Halloween2020Tarot(
        variable="xiv",
        title="xiv",
        roman="XIV",
        name="La Temperanza",
    ),
    Halloween2020Tarot(
        variable="xv",
        title="xv",
        roman="XV",
        name="Il Diavolo",
    ),
    Halloween2020Tarot(
        variable="xvi",
        title="xvi",
        roman="XVI",
        name="La Torre",
    ),
    Halloween2020Tarot(
        variable="xvii",
        title="xvii",
        roman="XVII",
        name="Le Stelle",
    ),
    Halloween2020Tarot(
        variable="xviii",
        title="xviii",
        roman="XVIII",
        name="La Luna",
    ),
    Halloween2020Tarot(
        variable="xix",
        title="xix",
        roman="XIX",
        name="Il Sole",
    ),
    Halloween2020Tarot(
        variable="xx",
        title="xx",
        roman="XX",
        name="Il Giudizio",
    ),
    Halloween2020Tarot(
        variable="xxi",
        title="xxi",
        roman="XII",
        name="Il Mondo",
        objective="Risolvi il mistero dei Trionfi Reali.",
        puzzle="""44°35'45.0"N 11°02'58.9"E""",
        check=None,
    ),
)
