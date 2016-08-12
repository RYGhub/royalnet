import requests
import json

file = open("db.json")
db = json.load(file)
file.close()

namelist = ["Cosimo03", "fedececco", "Il Gattopardo", "lordlake", "Luzcuzz", "MRdima98", "RYGFrankez",
            "Sensei the great", "UnsavouryComb2"]

for player in namelist:
    r = requests.get("https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/"
                     "{player}?api_key=d2e4cf8f-9a6d-4ce1-8eeb-6342c19f1ae4".format(player=player))
    r = r.json()[player.lower().replace(" ", "")]
    lolid = r["id"]
    print(str(lolid) + " | " + r["name"])
    discordid = str(input())
    db[discordid] = dict()
    db[discordid]["league"] = dict()
    db[discordid]["league"]["summonerid"] = lolid
    db[discordid]["league"]["region"] = "euw"
    db[discordid]["league"]["tier"] = -1
    db[discordid]["league"]["division"] = -1

file = open("db.json", "w")
json.dump(db, file)
file.close()
