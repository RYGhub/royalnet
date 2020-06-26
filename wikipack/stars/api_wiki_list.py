from typing import *
import datetime
import royalnet.constellation.api as rca
import royalnet.utils as ru
import royalnet.backpack.tables as rbt
from ..tables import *
import sqlalchemy as s


class ApiWikiListStar(rca.ApiStar):
    path = "/api/wiki/list/v2"

    tags = ["wiki"]

    parameters = {
        "get": {},
    }

    auth = {
        "get": False,
    }

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get the details of a specific Wiki page."""
        WikiRevisionT = self.alchemy.get(WikiRevision)

        lrs = await ru.asyncify(
            data.session
                .query(WikiRevisionT.page_id, s.func.max(WikiRevisionT.revision_id))
                .group_by(WikiRevisionT.page_id)
                .all
        )

        pages = []

        for page_id, revision_id in lrs:
            page = await ru.asyncify(
                data.session
                    .query(WikiRevisionT)
                    .get,
                (page_id, revision_id)
            )

            pages.append(page)

        return [r.json_list() for r in sorted(pages, key=lambda p: (p.category, p.title))]
