import royalnet.commands as rc


def get_interface_data(data: rc.CommandData):
    if data._interface.name == "telegram":
        return data.message.chat.id
    elif data._interface.name == "discord":
        return data.message.channel.id
    else:
        raise rc.UnsupportedError("This interface isn't supported yet.")
