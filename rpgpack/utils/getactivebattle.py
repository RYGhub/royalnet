from typing import *
from ..tables import DndActiveBattle
from ..utils import get_interface_data
import royalnet.utils as ru
import royalnet.commands as rc
import pickle


async def get_active_battle(*, data: rc.CommandData, session) -> Optional[DndActiveBattle]:
    alchemy = data.alchemy
    idata = get_interface_data(data)

    DndAcBaT = alchemy.get(DndActiveBattle)
    active_battles: List[DndActiveBattle] = await ru.asyncify(
        session
            .query(DndAcBaT)
            .filter_by(interface_name=data.command.serf.__class__.__name__)
            .all
    )

    for active_battle in active_battles:
        if data.command.serf.__class__.__name__ == "TelegramSerf":
            # interface_data is chat id
            chat_id = pickle.loads(active_battle.interface_data)
            if chat_id == idata:
                return active_battle
        elif data.command.serf.__class__.__name__ == "DiscordSerf":
            # interface_data is channel id
            chat_id = pickle.loads(active_battle.interface_data)
            if chat_id == idata:
                return active_battle
        else:
            raise rc.UnsupportedError("This interface isn't supported yet.")

    return None
