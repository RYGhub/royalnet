from typing import *
from .trionfoinfo import TrionfoInfo
from .check import *

trionfilist: List[TrionfoInfo] = [
    TrionfoInfo(
        variable="zero",
        title="o",
        roman="0",
        name="Il Folle",
        puzzle="UN VIAGGIO TI ATTENDE",
        objective="Trova la pagina dei Trionfi Reali.",
        check=NullCheck(),
    ),
    TrionfoInfo(
        variable="i",
        title="i",
        roman="I",
        name="Il Mago",
        puzzle="L'ULTIMO GIORNO",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/42910]Magicka[/url] "
                  "o [url=https://store.steampowered.com/app/238370]Magicka 2[/url].",
        check=CheckPlayedSteamGame(42910) or CheckPlayedSteamGame(238370),
    ),
    TrionfoInfo(
        variable="ii",
        title="ii",
        roman="II",
        name="L'Alta Sacerdotessa",
        puzzle="NEL DECIMO MESE",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/881100]Noita[/url].",
        check=CheckPlayedSteamGame(881100),
    ),
    TrionfoInfo(
        variable="iii",
        title="iii",
        roman="III",
        name="L'Imperatrice",
        puzzle="RIMANI LIBERO",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/245170]Skullgirls[/url].",
        check=CheckPlayedSteamGame(245170),
    ),
    TrionfoInfo(
        variable="iv",
        title="iv",
        roman="IV",
        name="L'Imperatore",
        puzzle="SEGUI GLI ORDINI",
        objective="Vinci una partita su [url=https://store.steampowered.com/app/611500]Quake Champions[/url].",
        check=CheckAchievementSteamGame(611500, "qc_victory")
    ),
    TrionfoInfo(
        variable="v",
        title="v",
        roman="V",
        name="Il Papa",
        puzzle="ALLA DECIMASESTA ORA",
        objective="Completa la prima zona di [url=https://store.steampowered.com/app/247080]Crypt of the Necrodancer["
                  "/url] con qualsiasi personaggio.",
        check=CheckAchievementSteamGame(247080, "ACH_ZONE1_COMPLETE")
    ),
    TrionfoInfo(
        variable="vi",
        title="vi",
        roman="VI",
        name="Gli Amanti",
        puzzle="ANCORA TRENTA MINUTI",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/698780]Doki Doki Literature Club["
                  "/url].",
        check=CheckPlayedSteamGame(698780),
    ),
    TrionfoInfo(
        variable="vii",
        title="vii",
        roman="VII",
        name="Il Carro",
        puzzle="SOPRA UN CARRO",
        objective="Gioca 5 incontri di [url=https://store.steampowered.com/app/326460/ShellShock_Live]ShellShock Live["
                  "/url].",
        check=CheckAchievementSteamGame(326460, "play5")
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
        objective="Gioca almeno mezz'ora ad [url=https://store.steampowered.com/app/945360]Among Us[/url] su Steam.",
        check=CheckPlayedSteamGame(945360)
    ),
    TrionfoInfo(
        variable="x",
        title="x",
        roman="X",
        name="La Fortuna",
        puzzle="LA CASA DEI GIOCHI",
        objective="Chiedi a Royal Bot di predire il tuo futuro.",
        check=NullCheck(),
    ),
    TrionfoInfo(
        variable="xi",
        title="xi",
        roman="XI",
        name="La Forza",
        puzzle="ALLA LIBERA ROCCAFORTE",
        objective="Gioca almeno mezz'ora ad [url=https://store.steampowered.com/app/57300]Amnesia: The Dark Descent["
                  "/url].",
        check=CheckPlayedSteamGame(57300)
    ),
    TrionfoInfo(
        variable="xii",
        title="xii",
        roman="XII",
        name="L'Appeso",
        puzzle="PORTA CAVI E ARNESI",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/381210]Dead by "
                  "Daylight.[/url]",
        check=CheckPlayedSteamGame(381210),
    ),
    TrionfoInfo(
        variable="xiii",
        title="xiii",
        roman="XIII",
        name="La Morte",
        puzzle="NON DIMENTICARE IL CIBO",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/322330]Don't Starve Together[/url].",
        check=CheckPlayedSteamGame(322330),
    ),
    TrionfoInfo(
        variable="xiv",
        title="xiv",
        roman="XIV",
        name="La Temperanza",
        puzzle="NIENTE ALCOOL",
        objective="Raggiungi la Tenuta dell'Antenato su [url=https://store.steampowered.com/app/262060]Darkest Dungeon["
                  "/url].",
        check=CheckAchievementSteamGame(262060, "welcome_home"),
    ),
    TrionfoInfo(
        variable="xv",
        title="xv",
        roman="XV",
        name="Il Diavolo",
        puzzle="GIOCA CON LUI",
        objective="Completa la prima missione di [url=https://store.steampowered.com/app/379720]DOOM[/url].",
        check=CheckAchievementSteamGame(379720, "ach_4")
    ),
    TrionfoInfo(
        variable="xvi",
        title="xvi",
        roman="XVI",
        name="La Torre",
        puzzle="CONQUISTA LA CIMA",
        objective="Sconfiggi un boss del primo piano su [url=https://store.steampowered.com/app/646570/]"
                  "Slay the Spire[/url].",
        check=CheckAchievementSteamGame(646570, "GUARDIAN") or CheckAchievementSteamGame(646570, "GHOST_GUARDIAN") or
              CheckAchievementSteamGame(646570, "SLIME_BOSS")
    ),
    TrionfoInfo(
        variable="xvii",
        title="xvii",
        roman="XVII",
        name="Le Stelle",
        puzzle="STAI IN COMPAGNIA",
        objective="Completa due missioni co-op online su ["
                  "url=https://store.steampowered.com/app/630/Alien_Swarm]Alien Swarm[/url].",
        check=CheckAchievementSteamGame(630, "ASW_PARA_HAT"),
    ),
    TrionfoInfo(
        variable="xviii",
        title="xviii",
        roman="XVIII",
        name="La Luna",
        puzzle="FINO ALLA UNA",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/388880]Oxenfree[/url].",
        check=CheckPlayedSteamGame(388880),
    ),
    TrionfoInfo(
        variable="xix",
        title="xix",
        roman="XIX",
        name="Il Sole",
        puzzle="IL TUO NOME SPLENDERÀ",
        objective="Gioca almeno mezz'ora a [url=https://store.steampowered.com/app/420530]OneShot[/url].",
        check=CheckPlayedSteamGame(420530),
    ),
    TrionfoInfo(
        variable="xx",
        title="xx",
        roman="XX",
        name="Il Giudizio",
        puzzle="E GIUDICHERÀ GLI ALTRI",
        objective="Completa la campagna Dead Center di [url=https://store.steampowered.com/app/550]"
                  "Left 4 Dead 2[/url].",
        check=CheckAchievementSteamGame(550, "ACH_SURVIVE_MALL"),
    ),
    TrionfoInfo(
        variable="xxi",
        title="xxi",
        roman="XXI",
        name="Il Mondo",
        puzzle="""44°35'45.0"N 11°02'58.9"E""",
        objective="Attraverso i Trionfi, il segreto sarà rivelato...",
        check=NullCheck(),
    ),
]