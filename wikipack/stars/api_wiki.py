from typing import *
import datetime
import royalnet.constellation.api as rca
import royalnet.utils as ru
import royalnet.backpack.tables as rbt
from ..tables import *


class ApiWikiStar(rca.ApiStar):
    path = "/api/wiki/v2"

    tags = ["wiki"]

    parameters = {
        "get": {
            "page_id": "The id of the wiki page to get the details of."
        },
        "post": {
            "category": "The category of the page.",
            "title": "The title of the page.",
            "contents": "The contents of the page.",
            "format": "(Optional) The format of the page. Default is 'gfm' for GitHub Flavored Markdown.",
            "role_to_view": "(Optional) The role required to view this page.\n\n"
                            "A * means unauthenticated users can view this page.\n\n"
                            "Be careful to not lock yourself out!",
            "role_to_edit": "(Optional) The role required to edit this page.\n\n"
                            "A * means unauthenticated users can edit this page.\n\n"
                            "Be careful to not lock yourself out!",
        },
        "put": {
            "page_id": "The id of the wiki page to create a new revision of.",
            "category": "The category of the page.",
            "title": "The title of the page.",
            "contents": "The contents of the page.",
            "format": "The format of the page. Default is 'gfm' for GitHub Flavored Markdown.",
            "role_to_view": "The role required to view this page.\n\n"
                            "A * means unauthenticated users can view this page.\n\n"
                            "Be careful to not lock yourself out!",
            "role_to_edit": "The role required to edit this page.\n\n"
                            "A * means unauthenticated users can edit this page.\n\n"
                            "Be careful to not lock yourself out!",
        },
        "delete": {
            "page_id": "The id of the wiki page to delete.",
        },
    }

    auth = {
        "get": True,
        "post": True,
        "put": True,
        "delete": True
    }

    @property
    def default_view_role(self) -> str:
        return self.config["roles"]["view"]

    async def can_view(self, user: rbt.User, lr: WikiRevision) -> bool:
        if lr.role_to_view == "*":
            return True

        if user is None:
            return False

        if lr.role_to_view in user.roles or self.admin_role in user.roles:
            return True
        return False

    @property
    def default_edit_role(self) -> str:
        return self.config["roles"]["edit"]

    async def can_edit(self, user: rbt.User, lr: WikiRevision) -> bool:
        if lr.role_to_edit == "*":
            return True

        if user is None:
            return False

        if lr.role_to_edit in user.roles or self.admin_role in user.roles:
            return True
        return False

    @property
    def create_role(self) -> str:
        return self.config["roles"]["create"]

    async def can_create(self, user: rbt.User) -> bool:
        if self.create_role == "*":
            return True

        if user is None:
            return False

        if self.create_role in user.roles or self.admin_role in user.roles:
            return True
        return False

    @property
    def delete_role(self) -> str:
        return self.config["roles"]["delete"]

    async def can_delete(self, user: rbt.User) -> bool:
        if self.delete_role == "*":
            return True

        if user is None:
            return False

        if self.delete_role in user.roles or self.admin_role in user.roles:
            return True
        return False

    @property
    def admin_role(self) -> str:
        return self.config["roles"]["admin"]

    async def find_lr(self, data: rca.ApiData) -> WikiRevision:
        WikiRevisionT = self.alchemy.get(WikiRevision)

        page_id = data.int("page_id")

        lr: WikiRevision = await ru.asyncify(
            data.session
                .query(WikiRevisionT)
                .filter_by(page_id=page_id)
                .order_by(WikiRevisionT.revision_id.desc())
                .first
        )

        if lr is None:
            raise rca.NotFoundError(f"No page found with the id `{page_id}`.")

        return lr

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get the details of a specific Wiki page."""
        lr = await self.find_lr(data)

        try:
            user = await data.user()
        except rca.MissingParameterError:
            user = None

        if not await self.can_view(user, lr):
            raise rca.ForbiddenError(f"Viewing this page requires the `{lr.role_to_view}` role.")

        return lr.json()

    @rca.magic
    async def post(self, data: rca.ApiData) -> ru.JSON:
        """Create a new Wiki page."""
        WikiRevisionT = self.alchemy.get(WikiRevision)

        try:
            user = await data.user()
        except rca.MissingParameterError:
            user = None

        if not await self.can_create(user):
            raise rca.ForbiddenError(f"Creating a new page requires the `{self.create_role}` role.")

        category = data.str("category", optional=False)
        title = data.str("title", optional=False)
        contents = data.str("contents", optional=False)
        format_ = data.str("format", optional=True)
        role_to_view = data.str("role_to_view", optional=True)
        role_to_edit = data.str("role_to_edit", optional=True)

        nr: WikiRevision = WikiRevisionT(
            category=category,
            title=title,
            contents=contents,
            format=format_ or "gfm",
            author=user,
            timestamp=datetime.datetime.now(),
            role_to_view=role_to_view or self.default_view_role,
            role_to_edit=role_to_edit or self.default_edit_role,
        )

        data.session.add(nr)
        await data.session_commit()

        return nr.json()

    @rca.magic
    async def put(self, data: rca.ApiData) -> ru.JSON:
        """Edit a specific Wiki page, creating a new revision."""
        WikiRevisionT = self.alchemy.get(WikiRevision)

        lr = await self.find_lr(data)

        try:
            user = await data.user()
        except rca.MissingParameterError:
            user = None

        if not await self.can_edit(user, lr):
            raise rca.ForbiddenError(f"Editing this page requires the `{lr.role_to_edit}` role.")

        category = data.str("category", optional=True)
        title = data.str("title", optional=True)
        contents = data.str("contents", optional=True)
        format_ = data.str("format", optional=True)
        role_to_view = data.str("role_to_view", optional=True)
        role_to_edit = data.str("role_to_edit", optional=True)

        nr: WikiRevision = WikiRevisionT(
            page_id=lr.page_id,
            category=category or lr.category,
            title=title or lr.title,
            contents=contents or lr.contents,
            format=format_ or lr.format,
            author=user,
            timestamp=datetime.datetime.now(),
            role_to_view=role_to_view or lr.role_to_view,
            role_to_edit=role_to_edit or lr.role_to_edit,
        )

        data.session.add(nr)
        await data.session_commit()

        return nr.json()

    @rca.magic
    async def delete(self, data: rca.ApiData) -> ru.JSON:
        """Delete a specific Wiki page and all its revisions."""
        WikiRevisionT = self.alchemy.get(WikiRevision)
        WikiDeletionT = self.alchemy.get(WikiDeletion)

        lr = await self.find_lr(data)

        try:
            user = await data.user()
        except rca.MissingParameterError:
            user = None

        if not await self.can_delete(user):
            raise rca.ForbiddenError(f"Deleting pages requires the `{self.delete_role}` role.")

        deletion = WikiDeletionT(
            page_id=lr.page_id,
            deleted_by=user,
            timestamp=datetime.datetime.now(),
        )

        pages = await ru.asyncify(
            data.session.query(WikiRevisionT).filter_by(page_id=lr.page_id).all
        )
        for page in pages:
            data.session.delete(page)
        data.session.add(deletion)

        await data.session_commit()

        return deletion.json()
