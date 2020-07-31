## The utils folder

The utils folder should contain the utility functions and classes that your Pack uses.

Its contents are imported **before** the commands, events and stars but **after** the tables, so **you can't import them** in the files contained in the `tables` folder, or you will create a [circular import](https://stackabuse.com/python-circular-imports/)!

Files in this folder are **forbidden from importing modules** from the `commands`, `events` and `stars` folders, as that will create a circular import too.
