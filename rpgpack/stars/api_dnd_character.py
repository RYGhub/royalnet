import royalnet.utils as ru
import royalnet.constellation.api as rca
from ..tables import DndCharacter


class ApiDndCharacterStar(rca.ApiStar):
    path = "/api/dnd/character/v2"

    parameters = {
        "get": {
            "character_id": "The id of the character to get."
        }
    }

    tags = ["dnd"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> dict:
        """Get the character sheet of a specific D&D Character."""
        DndCharacterT = self.alchemy.get(DndCharacter)

        character_id = data["character_id"]

        character = await ru.asyncify(
            data.session
                .query(DndCharacterT)
                .filter_by(character_id=character_id)
                .one_or_none
        )

        if character is None:
            raise rca.NotFoundError(f"No character with id '{character_id}' found")

        return character.json()
