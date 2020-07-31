## The types folder

The types folder should contain the enums and custom types that are used in your tables.

Please note that the contents of this folder are imported **before** everything else in the pack.

Its contents **can be imported anywhere** in the Pack, including the `tables` folder, without creating a circular import.

However, its files are **forbidden from importing anything else** from the rest of the pack!
