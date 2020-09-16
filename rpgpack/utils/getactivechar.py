from typing import *
from ..tables import DndActiveCharacter
from ..utils import get_interface_data
import royalnet.utils as ru
import royalnet.commands as rc
import pickle


async def get_active_character(*, data: rc.CommandData, session) -> Optional[DndActiveCharacter]:
    alchemy = data.alchemy
    user = await data.find_author(session=session, required=True)
    idata = get_interface_data(data)

    DndAcChT = alchemy.get(DndActiveCharacter)
    active_characters: List[DndActiveCharacter] = await ru.asyncify(
        session
        .query(DndAcChT)
        .filter_by(interface_name=data.command.serf.__class__.__name__, user=user)
        .all
    )

    for active_character in active_characters:
        if data.command.serf.__class__.__name__ == "TelegramSerf":
            # interface_data is chat id
            chat_id = pickle.loads(active_character.interface_data)
            if chat_id == idata:
                return active_character
        elif data.command.serf.__class__.__name__ == "DiscordSerf":
            # interface_data is channel id
            chat_id = pickle.loads(active_character.interface_data)
            if chat_id == idata:
                return active_character
        else:
            raise rc.UnsupportedError("This interface isn't supported yet.")

    return None
