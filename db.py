import json
import filemanager

db = json.loads(filemanager.readfile("db.json"))


def findbyname(name: str):
    for player in db:
        if db[player]["telegram"]["username"] == name:
            return db[player]
    else:
        return None


# def findbykey(key, value):
#     for player in db:
#         if player[key] == value:
#             return db[player]
#     else:
#         return None

