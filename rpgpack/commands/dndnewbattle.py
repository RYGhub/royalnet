from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import DndBattle


class DndnewbattleCommand(rc.Command):
    name: str = "dndnewbattle"

    description: str = "Create a new D&D battle."

    syntax: str = "{name}\n[description]"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        BattleT = self.alchemy.get(DndBattle)

        line_args = args.joined(require_at_least=1).split("\n", 1)
        name = line_args[0]
        description = line_args[1] if len(line_args) > 1 else None

        async with data.session_acm() as session:
            battle = BattleT(
                name=name,
                description=description
            )

            session.add(battle)
            await ru.asyncify(session.commit)

            await data.reply(f"✅ Battle [b]{battle.name}[/b] (ID: {battle.id}) created!")
