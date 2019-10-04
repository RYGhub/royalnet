import typing
import pickle
import discord
from ..command import Command
from ..commandinterface import CommandInterface
from ..commandargs import CommandArgs
from ..commanddata import CommandData
from ...utils import NetworkHandler
from ...network import Request, ResponseSuccess
from ..commanderrors import CommandError
from ...audio.playmodes import Playlist, Pool, Layers
if typing.TYPE_CHECKING:
    from ...bots import DiscordBot


class PlaymodeNH(NetworkHandler):
    message_type = "music_playmode"

    @classmethod
    async def discord(cls, bot: "DiscordBot", data: dict):
        """Handle a playmode Royalnet request. That is, change current PlayMode."""
        # Find the matching guild
        if data["guild_name"]:
            guilds: typing.List[discord.Guild] = bot.client.find_guild_by_name(data["guild_name"])
        else:
            guilds = bot.client.guilds
        if len(guilds) == 0:
            raise CommandError("No guilds with the specified name found.")
        if len(guilds) > 1:
            raise CommandError("Multiple guilds with the specified name found.")
        guild = list(bot.client.guilds)[0]
        # Delete the previous PlayMode, if it exists
        if bot.music_data[guild] is not None:
            bot.music_data[guild].delete()
        # Create the new PlayMode
        if data["mode_name"] == "playlist":
            bot.music_data[guild] = Playlist()
        elif data["mode_name"] == "pool":
            bot.music_data[guild] = Pool()
        elif data["mode_name"] == "layers":
            bot.music_data[guild] = Layers()
        else:
            raise CommandError("Unknown PlayMode specified.")
        return ResponseSuccess()


class PlaymodeCommand(Command):
    name: str = "playmode"

    description: str = "Cambia modalità di riproduzione per la chat vocale."

    syntax = "[ [guild] ] (mode)"

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        interface.register_net_handler(PlaymodeNH.message_type, PlaymodeNH)

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        guild_name, mode_name = args.match(r"(?:\[(.+)])?\s*(\S+)\s*")
        await self.interface.net_request(Request(PlaymodeNH.message_type, {"mode_name": mode_name,
                                                                           "guild_name": guild_name}),
                                         "discord")
        await data.reply(f"🔃 Impostata la modalità di riproduzione a: [c]{mode_name}[/c].")
