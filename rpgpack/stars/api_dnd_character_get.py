from royalnet.utils import *
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import DndCharacter


class ApiDndCharacterGetStar(ApiStar):
    path = "/api/dnd/character/get/v1"

    summary = "Get a D&D Character."

    parameters = {
        "character_id": "The id of the character to get."
    }

    tags = ["dnd"]

    async def api(self, data: ApiData) -> dict:
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
