import royalnet.commands as rc


def get_interface_data(data: rc.CommandData):
    if data.command.serf.__class__.__name__ == "TelegramSerf":
        return data.message.chat.id
    if data.command.serf.__class__.__name__ == "DiscordSerf":
        return data.message.channel.id
    else:
        raise rc.UnsupportedError("This interface isn't supported yet.")
