import asyncio
import discord
import json
import overwatch
import strings as s

loop = asyncio.get_event_loop()
d_client = discord.Client()

# Get player database from the db.json file
file = open("db.json")
db = json.load(file)
file.close()

# Get the discord bot token from "discordtoken.txt"
file = open("discordtoken.txt", "r")
token = file.read()
file.close()

# Every 300 seconds, update player status and check for levelups
async def overwatch_level_up(timeout):
    while True:
        # Update data for every player in list
        for player in db:
            if db[player]["overwatch"] is not None:
                r = await overwatch.get_player_data(**db[player]["overwatch"])
                if r["data"]["level"] > db[player]["overwatch"]["level"]:
                    # Convert user ID into a mention
                    user = "<@" + player + ">"
                    # Prepare the message to send
                    msg = s.overwatch_level_up.format(player=user, level=r["data"]["level"])
                    # Send the message to the discord channel
                    loop.create_task(d_client.send_message(d_client.get_channel("213655027842154508"), msg))
                    db[player]["overwatch"]["level"] = r["data"]["level"]
                    # Update database
                    f = open("db.json", "w")
                    json.dump(db, f)
                    f.close()
        # Wait for the timeout
        await asyncio.sleep(timeout)

loop.create_task(overwatch_level_up(30))
d_client.run(token)
