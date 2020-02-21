from typing import *
import royalnet
import royalnet.commands as rc
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

        battle = BattleT(
            name=name,
            description=description
        )

        data.session.add(battle)
        await data.session_commit()

        await data.reply(f"✅ Battaglia [b]{battle.name}[/b] creata!")
