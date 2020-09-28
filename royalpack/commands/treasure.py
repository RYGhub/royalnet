from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import Treasure, FiorygiTransaction


class TreasureCommand(rc.Command):
    name: str = "treasure"

    description: str = "Riscatta un Treasure che hai trovato da qualche parte."

    syntax: str = "{code}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        TreasureT = self.alchemy.get(Treasure)

        async with data.session_acm() as session:
            author = await data.find_author(session=session, required=True)
            code = args[0].lower()

            treasure = await ru.asyncify(session.query(TreasureT).get, code)
            if treasure is None:
                raise rc.UserError("Non esiste nessun Treasure con quel codice.")
            if treasure.redeemed_by is not None:
                raise rc.UserError(f"Quel tesoro è già stato riscattato da {treasure.redeemed_by}.")

            treasure.redeemed_by = author
            await ru.asyncify(session.commit)
            await FiorygiTransaction.spawn_fiorygi(author,
                                                   treasure.value,
                                                   f'aver trovato il tesoro "{treasure.code}"',
                                                   data=data,
                                                   session=session)
            await data.reply("🤑 Tesoro riscattato!")
