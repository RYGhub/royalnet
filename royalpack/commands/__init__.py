# Imports go here!
from .ahnonlosoio import AhnonlosoioCommand
from .answer import AnswerCommand
from .brawlhalla import BrawlhallaCommand
from .cat import CatCommand
from .ciaoruozi import CiaoruoziCommand
from .color import ColorCommand
from .cv import CvCommand
from .cvstats import CvstatsCommand
from .diario import DiarioCommand
from .diarioquote import DiarioquoteCommand
from .diarioshuffle import DiarioshuffleCommand
from .dota import DotaCommand
from .eat import EatCommand
from .emojify import EmojifyCommand
from .eval import EvalCommand
from .exec import ExecCommand
from .fortune import FortuneCommand
from .givefiorygi import GivefiorygiCommand
from .givetreasure import GivetreasureCommand
from .help import HelpCommand
from .leagueoflegends import LeagueoflegendsCommand
from .magickfiorygi import MagickfiorygiCommand
from .magicktreasure import MagicktreasureCommand
from .matchmaking import MatchmakingCommand
from .ping import PingCommand
from .pmots import PmotsCommand
from .dog import DogCommand
from .rage import RageCommand
from .reminder import ReminderCommand
from .royalpackversion import RoyalpackCommand
from .ship import ShipCommand
from .smecds import SmecdsCommand
from .spell import SpellCommand
from .steammatch import SteammatchCommand
from .steampowered import SteampoweredCommand
from .treasure import TreasureCommand
from .trivia import TriviaCommand
from .osu import OsuCommand
from .trionfireali import TrionfirealiCommand

# Enter the commands of your Pack here!
available_commands = [
    AhnonlosoioCommand,
    AnswerCommand,
    BrawlhallaCommand,
    CatCommand,
    CiaoruoziCommand,
    ColorCommand,
    CvCommand,
    CvstatsCommand,
    DiarioCommand,
    DiarioquoteCommand,
    DiarioshuffleCommand,
    DotaCommand,
    EatCommand,
    EmojifyCommand,
    EvalCommand,
    ExecCommand,
    FortuneCommand,
    GivefiorygiCommand,
    GivetreasureCommand,
    HelpCommand,
    LeagueoflegendsCommand,
    MagickfiorygiCommand,
    MagicktreasureCommand,
    MatchmakingCommand,
    PingCommand,
    PmotsCommand,
    DogCommand,
    RageCommand,
    ReminderCommand,
    RoyalpackCommand,
    ShipCommand,
    SmecdsCommand,
    SpellCommand,
    SteammatchCommand,
    SteampoweredCommand,
    TreasureCommand,
    TriviaCommand,
    OsuCommand,
    TrionfirealiCommand,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_commands]
