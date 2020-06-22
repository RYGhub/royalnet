from royalnet.utils import *
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import DndCharacter


class ApiDndCharacterStar(ApiStar):
    path = "/api/dnd/character/v2"

    parameters = {
        "get": {
            "character_id": "The id of the character to get."
        }
    }

    tags = ["dnd"]

    async def get(self, data: ApiData) -> dict:
        """Get the character sheet of a specific D&D Character."""
        DndCharacterT = self.alchemy.get(DndCharacter)

        character_id = data["character_id"]

        character = await asyncify(
            data.session
                .query(DndCharacterT)
                .filter_by(character_id=character_id)
                .one_or_none
        )

        if character is None:
            raise NotFoundError(f"No character with id '{character_id}' found")

        return character.json()
