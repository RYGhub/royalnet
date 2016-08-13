import asyncio
import discord
import json
import overwatch
import league
import strings as s
import telegram

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

# Every timeout seconds, update player status and check for levelups
async def overwatch_level_up(timeout):
    while True:
        # Wait for the timeout
        await asyncio.sleep(timeout)
        print("Checking for Overwatch updates.")
        # Update data for every player in list
        for player in db:
            if "overwatch" in db[player]:
                r = await overwatch.get_player_data(**db[player]["overwatch"])
                if r["data"]["level"] > db[player]["overwatch"]["level"]:
                    # Convert user ID into a mention
                    user = "<@" + player + ">"
                    # Prepare the message to send
                    msg = s.overwatch_level_up.format(player=user, level=r["data"]["level"])
                    # Send the message to the discord channel
                    loop.create_task(d_client.send_message(d_client.get_channel("213655027842154508"), msg))
                    # Send the message to the telegram group chat
                    loop.create_task(telegram.send_message(msg, -2141322))
                    # Update database
                    db[player]["overwatch"]["level"] = r["data"]["level"]
                    f = open("db.json", "w")
                    json.dump(db, f)
                    f.close()
        print("Check for Overwatch completed.")

# Every timeout seconds, update player league and check for rank changes
async def league_rank_change(timeout):
    while True:
        # Wait for the timeout
        await asyncio.sleep(timeout)
        print("Checking for League of Legends updates.")
        # Update data for every player in list
        for player in db:
            if "league" in db[player]:
                try:
                    r = await league.get_player_rank(**db[player]["league"])
                except league.NoRankedGamesCompletedException:
                    # If the player has no ranked games completed, skip him
                    continue
                else:
                    # Convert tier into a number
                    tier_number = league.ranklist.index(r["tier"])
                    roman_number = league.roman.index(r["entries"][0]["division"])
                    # Check for tier changes
                    if tier_number != db[player]["league"]["tier"] or roman_number != db[player]["league"]["division"]:
                        # Convert user ID into a mention
                        user = "<@" + player + ">"
                        # Prepare the message to send
                        msg = s.league_rank_up.format(player=user,
                                                      tier=s.league_tier_list[tier_number],
                                                      division=r["entries"][0]["division"])
                        # Send the message to the discord channel
                        loop.create_task(d_client.send_message(d_client.get_channel("213655027842154508"), msg))
                        # Send the message to the telegram group chat
                        loop.create_task(telegram.send_message(msg, -2141322))
                        # Update database
                        db[player]["league"]["tier"] = tier_number
                        db[player]["league"]["division"] = roman_number
                        f = open("db.json", "w")
                        json.dump(db, f)
                        f.close()
        print("Check for League of Legends completed.")

print("Added Overwatch to the queue.")
loop.create_task(overwatch_level_up(900))
print("Added League of Legends to the queue.")
loop.create_task(league_rank_change(900))

try:
    loop.run_until_complete(d_client.start(token))
except KeyboardInterrupt:
    loop.run_until_complete(d_client.logout())
    # cancel all tasks lingering
finally:
    loop.close()
