from .trionfoinfo import TrionfoInfo
from .check import *

trionfilist = (
    TrionfoInfo(
        variable="zero",
        title="o",
        roman="0",
        name="Il Folle",
        puzzle="IL DESTINO TI ATTENDE",
        objective="Partecipa ai Trionfi Reali.",
        check=None,
    ),
    TrionfoInfo(
        variable="i",
        title="i",
        roman="I",
        name="Il Mago",
        puzzle="L'ULTIMO GIORNO",
        objective="Trova una /spell che possa fare almeno 250 danni.",
        check=None,
    ),
    TrionfoInfo(
        variable="ii",
        title="ii",
        roman="II",
        name="La Sacerdotessa",
        puzzle="DEL DECIMO MESE",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/881100]Noita[/url].",
        check=CheckPlayedSteamGame(881100),
    ),
    TrionfoInfo(
        variable="iii",
        title="iii",
        roman="III",
        name="L'Imperatrice",
        puzzle="NON IMPEGNARTI",
        objective="Gioca almeno mezz'ora [url=https://store.steampowered.com/app/245170]Skullgirls[/url].",
        check=CheckPlayedSteamGame(245170),
    ),
    TrionfoInfo(
        variable="iv",
        title="iv",
        roman="IV",
        name="L'Imperatore",
        puzzle="ESEGUI GLI ORDINI",
        objective="Vinci una partita su [url=https://store.steampowered.com/app/611500]Quake Champions[/url].",
        check=CheckAchievementSteamGame(611500, "qc_victory")
    ),
    TrionfoInfo(
        variable="v",
        title="v",
        roman="V",
        name="Il Papa",
        puzzle="ALLA SEDICESIMA ORA",
    ),
    TrionfoInfo(
        variable="vi",
        title="vi",
        roman="VI",
        name="Gli Amanti",
        puzzle="PIÙ DIECI MINUTI",
        objective="Finisci l'Atto 3 di [url=https://store.steampowered.com/app/698780]Doki Doki Literature Club["
                  "/url].",
        check=CheckPlayedSteamGame(698780),
    ),
    TrionfoInfo(
        variable="vii",
        title="vii",
        roman="VII",
        name="Il Carro",
        puzzle="SOPRA UN CARRO",
    ),
    TrionfoInfo(
        variable="viii",
        title="viii",
        roman="VIII",
        name="La Giustizia",
        puzzle="RAGGIUNGI",
        objective="Porta la giustizia dalla tua parte su [url=https://store.steampowered.com/app/1289310]Helltaker["
                  "/url].",
        check=CheckAchievementSteamGame(1289310, "achiev_05"),
    ),
    TrionfoInfo(
        variable="ix",
        title="ix",
        roman="IX",
        name="L'Eremita",
        puzzle="SEGRETAMENTE",
    ),
    TrionfoInfo(
        variable="x",
        title="x",
        roman="X",
        name="La Fortuna",
        puzzle="LA CASA DEI GIOCHI"
    ),
    TrionfoInfo(
        variable="xi",
        title="xi",
        roman="XI",
        name="La Forza",
    ),
    TrionfoInfo(
        variable="xii",
        title="xii",
        roman="XII",
        name="L'Appeso",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/381210]Dead by "
                  "Daylight.[/url]",
        check=CheckPlayedSteamGame(381210),
    ),
    TrionfoInfo(
        variable="xiii",
        title="xiii",
        roman="XIII",
        name="La Morte",
        objective="Raggiungi la Tenuta dell'Antenato su [url=https://store.steampowered.com/app/262060]Darkest Dungeon["
                  "/url].",
        check=CheckAchievementSteamGame(262060, "welcome_home"),
    ),
    TrionfoInfo(
        variable="xiv",
        title="xiv",
        roman="XIV",
        name="La Temperanza",
    ),
    TrionfoInfo(
        variable="xv",
        title="xv",
        roman="XV",
        name="Il Diavolo",
    ),
    TrionfoInfo(
        variable="xvi",
        title="xvi",
        roman="XVI",
        name="La Torre",
        objective="Sconfiggi un boss del secondo piano su [url=https://store.steampowered.com/app/646570/]"
                  "Slay the Spire[/url].",
        check=CheckAchievementSteamGame(646570, "AUTOMATON") or CheckAchievementSteamGame(646570, "COLLECTOR") or
              CheckAchievementSteamGame(646570, "CHAMP")
    ),
    TrionfoInfo(
        variable="xvii",
        title="xvii",
        roman="XVII",
        name="Le Stelle",
    ),
    TrionfoInfo(
        variable="xviii",
        title="xviii",
        roman="XVIII",
        name="La Luna",
        objective="Gioca a [url=https://store.steampowered.com/app/388880]Oxenfree[/url].",
        check=CheckPlayedSteamGame(388880),
    ),
    TrionfoInfo(
        variable="xix",
        title="xix",
        roman="XIX",
        name="Il Sole",
    ),
    TrionfoInfo(
        variable="xx",
        title="xx",
        roman="XX",
        name="Il Giudizio",
    ),
    TrionfoInfo(
        variable="xxi",
        title="xxi",
        roman="XII",
        name="Il Mondo",
        puzzle="""44°35'45.0"N 11°02'58.9"E""",
        objective="Risolvi il mistero dei Trionfi Reali.",
        check=None,
    ),
)