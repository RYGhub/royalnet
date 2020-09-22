import royalnet.backpack.tables as rbt
import royalnet.constellation.api as rca


class ApiUserRygStar(rca.ApiStar):
    path = "/api/user/ryg/v2"

    parameters = {
        "get": {
            "uid": "(Choose one) The id of the user to get information about.",
            "alias": "(Choose one) The alias of the user to get information about.",
        }
    }

    tags = ["user"]

    async def get_user(self, data: rca.ApiData):
        uid = data.int("uid", optional=True)
        alias = data.str("alias", optional=True)

        if uid:
            user = await rbt.User.find(self.alchemy, data.session, uid)
        elif alias:
            user = await rbt.User.find(self.alchemy, data.session, alias)
        else:
            raise rca.MissingParameterError("Neither uid or alias were specified.")

        if user is None:
            raise rca.NotFoundError("No such user.")

        return user

    @rca.magic
    async def get(self, data: rca.ApiData) -> dict:
        """Get Royalpack information about a user."""
        user = await self.get_user(data)
        result = {
            **user.json(),
            "bio": user.bio.json() if user.bio is not None else None,
            "fiorygi": user.fiorygi.fiorygi if user.fiorygi is not None else None,
            "steam": [steam.json() for steam in user.steam],
            "leagueoflegends": [leagueoflegends.json() for leagueoflegends in user.leagueoflegends],
            "osu": [osu.json() for osu in user.osu],
            "trivia": user.trivia_score.json() if user.trivia_score is not None else None,
        }
        return result
