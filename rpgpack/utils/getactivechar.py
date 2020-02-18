from typing import *
from ..tables import DndActiveCharacter
import royalnet.utils as ru
import royalnet.commands as rc
import pickle


def get_interface_data(data: rc.CommandData):
    if data._interface.name == "telegram":
        return data.message.chat.id
    elif data._interface.name == "discord":
        return data.message.channel.id
    else:
        raise rc.UnsupportedError("This interface isn't supported yet.")


async def get_active_character(data: rc.CommandData) -> Optional[DndActiveCharacter]:
    interface = data._interface
    alchemy = interface.alchemy
    user = await data.get_author(error_if_none=True)
    idata = get_interface_data(data)

    DndAcChT = alchemy.get(DndActiveCharacter)
    active_characters: List[DndActiveCharacter] = await ru.asyncify(
        data.session
            .query(DndAcChT)
            .filter_by(interface_name=interface.name, user=user)
            .all
    )

    for active_character in active_characters:
        if interface.name == "telegram":
            # interface_data is chat id
            chat_id = pickle.loads(active_character.interface_data)
            if chat_id == idata:
                return active_character
        elif interface.name == "discord":
            # interface_data is channel id
            chat_id = pickle.loads(active_character.interface_data)
            if chat_id == idata:
                return active_character
        else:
            raise rc.UnsupportedError("This interface isn't supported yet.")

    return None
