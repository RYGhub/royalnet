from starlette.responses import *
import royalnet.utils as ru
import royalnet.backpack.tables as rbt
import royalnet.constellation.api as rca


class ApiUserRygListStar(rca.ApiStar):
    path = "/api/user/ryg/list/v1"

    tags = ["user"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get Royalpack information about all users."""
        users: typing.List[rbt.User] = await ru.asyncify(
            data.session.query(self.alchemy.get(rbt.User)).all
        )
        return [{
            **user.json(),
            "bio": user.bio.json() if user.bio is not None else None,
            "fiorygi": user.fiorygi.fiorygi if user.fiorygi is not None else None,
            "steam": [steam.json() for steam in user.steam],
            "leagueoflegends": [leagueoflegends.json() for leagueoflegends in user.leagueoflegends],
            "osu": [osu.json() for osu in user.osu],
            "trivia": user.trivia_score.json() if user.trivia_score is not None else None,
        } for user in users if "member" in user.roles]
