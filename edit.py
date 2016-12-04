import json
import requests

file = open("leaguetoken.txt", "r")
token = file.read()
file.close()

# Get lol info, ported from league.py
def get_player_info(region: str, summonerid: int):
    # GET the json API response
    r = requests.get('https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/{summonerid}?api_key={token}'.format(region=region, summonerid=summonerid, token=token))
    # Ensure the request is successful
    if r.status_code == 200:
        return r.json()[str(summonerid)]
    elif r.status_code == 429:
        raise Exception("You've been ratelimited by Riot. Check your developer dashboard.")
    else:
        raise Exception("Unhandled API response.")

# Get player database from the db.json file
file =  open("db.json")
db = json.load(file)
file.close()

while True:
    # Select an user
    selection = input("Discord ID: ")
    # Quit and update database
    if selection == "":
        f = open("db.json", "w")
        json.dump(db, f)
        f.close()
        break
    # If player doesn't exists, add it to the db
    if selection not in db:
        print("Creating new user.")
        # Overwatch data
        data = input("Overwatch | platform region battletag: ")
        if data != "":
            splitted = data.split(" ")
            db[selection]["overwatch"] = {
                "platform": splitted[0],
                "region": splitted[1],
                "battletag": splitted[2]
            }
        # League of Legends data
        data = input("League | region username: ")
        if data != "":
            splitted = data.split(" ", 1)
            info = get_player_info(splitted[0], splitted[1])
            db[selection]["league"] = {
                "summonerid": info['id'],
                "region": splitted[0]
            }
        # Telegram data
        data = input("Telegram | username: ")
        if data != "":
            splitted = data.split(" ")
            db[selection]["telegram"] = {
                "username": splitted[0]
            }