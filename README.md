# `wikipack`

This pack adds a small Wiki to Royalnet, allowing communities to create their own small Wikis.

## Configuration options

```toml
[Packs."wikipack"]

# The roles that are authorized by default to complete certain actions.
# Setting them to * disables the authentication requirement, allowing unauthenticated users that privilege
[Packs."wikipack".roles]

# Users with this role will be able to view wiki pages that do not have a different role set.
view = "*"

# Users with this role will be able to create new wiki pages.
create = "wiki_create"

# Users with this role will be able to edit wiki pages that do not have a different role set.
edit = "wiki_edit"

# Users with this role will be able to delete wiki pages.
delete = "wiki_delete"

# Users with this role will override all other privileges.
admin = "wiki_admin"
```
