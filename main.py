import asyncio
import discord
import json
import overwatch
import league
import strings as s
import telegram
import bs4
import brawlhalla

loop = asyncio.get_event_loop()
d_client = discord.Client()
discord_is_ready = False


# When Discord is ready, set discord_is_ready to True
@d_client.event
async def on_ready():
    global discord_is_ready
    discord_is_ready = True

# Get player database from the db.json file
file = open("db.json")
db = json.load(file)
file.close()

# Get the discord bot token from "discordtoken.txt"
file = open("discordtoken.txt", "r")
token = file.read()
file.close()

# Every timeout seconds, update player status and check for levelups
async def overwatch_status_change(timeout):
    while True:
        if discord_is_ready:
            print("[Overwatch] Starting check...")
            # Update data for every player in list
            for player in db:
                if "overwatch" in db[player]:
                    try:
                        r = await overwatch.get_player_data(**db[player]["overwatch"])
                    except overwatch.NotFoundException:
                        print("[Overwatch] Player not found.")
                    except Exception:
                        # If some other error occours, skip the player
                        print("[Overwatch] Request returned an unhandled exception.")
                    else:
                        # Check for levelups
                        if "level" not in db[player]["overwatch"] \
                                or r["data"]["level"] > db[player]["overwatch"]["level"]:
                            # Send the message
                            loop.create_task(send_event(eventmsg=s.overwatch_level_up,
                                                        player=player,
                                                        level=r["data"]["level"]))
                            # Update database
                            db[player]["overwatch"]["level"] = r["data"]["level"]
                            f = open("db.json", "w")
                            json.dump(db, f)
                            f.close()
                        # Check for rank changes
                        if r["data"]["competitive"]["rank"] is not None:
                            if "rank" not in db[player]["overwatch"] \
                                    or int(r["data"]["competitive"]["rank"]) != db[player]["overwatch"]["rank"]:
                                # Send the message
                                loop.create_task(send_event(eventmsg=s.overwatch_rank_change,
                                                            player=player,
                                                            oldmedal=overwatch.rank_to_medal(
                                                                db[player]["overwatch"]["rank"]),
                                                            oldrank=db[player]["overwatch"]["rank"],
                                                            rank=int(r["data"]["competitive"]["rank"]),
                                                            medal=overwatch.rank_to_medal(
                                                                int(r["data"]["competitive"]["rank"]))))
                                # Update database
                                db[player]["overwatch"]["rank"] = r["data"]["competitive"]["rank"]
                                f = open("db.json", "w")
                                json.dump(db, f)
                                f.close()
                    finally:
                        asyncio.sleep(1)
            print("[Overwatch] Check completed successfully.")
            # Wait for the timeout
            await asyncio.sleep(timeout)
        else:
            await asyncio.sleep(1)

# Every timeout seconds, update player league and check for rank changes
async def league_rank_change(timeout):
    while True:
        if discord_is_ready:
            print("[League] Starting check for rank changes...")
            # Update data for every player in list
            for player in db:
                if "league" in db[player]:
                    try:
                        r = await league.get_player_rank(**db[player]["league"])
                    except league.NoRankedGamesCompletedException:
                        # If the player has no ranked games completed, skip him
                        pass
                    except league.RateLimitException:
                        # If you've been ratelimited, skip the player and notify the console.
                        print("[League] Request rejected for rate limit.")
                    except Exception:
                        # If some other error occours, skip the player
                        print("[League] Request returned an unhandled exception.")
                    else:
                        # Convert tier into a number
                        tier_number = league.ranklist.index(r["tier"])
                        roman_number = league.roman.index(r["entries"][0]["division"])
                        # Check for tier changes
                        if tier_number != db[player]["league"]["tier"] \
                                or roman_number != db[player]["league"]["division"]:
                            # Send the message
                            loop.create_task(send_event(eventmsg=s.league_rank_up,
                                                        player=player,
                                                        tier=s.league_tier_list[tier_number],
                                                        division=r["entries"][0]["division"],
                                                        oldtier=s.league_tier_list[db[player]["league"]["tier"]],
                                                        olddivision=
                                                        s.league_roman_list[db[player]["league"]["division"]]))
                            # Update database
                            db[player]["league"]["tier"] = tier_number
                            db[player]["league"]["division"] = roman_number
                            f = open("db.json", "w")
                            json.dump(db, f)
                            f.close()
                    finally:
                        # Prevent getting ratelimited by Riot
                        await asyncio.sleep(2)
            print("[League] Rank check completed.")
            # Wait for the timeout
            await asyncio.sleep(timeout)
        else:
            await asyncio.sleep(1)

# Every timeout seconds, update player level and check for changes
async def league_level_up(timeout):
    while True:
        if discord_is_ready:
            print("[League] Starting check for level changes...")
            # Update data for every player in list
            for player in db:
                if "league" in db[player]:
                    try:
                        r = await league.get_player_info(**db[player]["league"])
                    except league.RateLimitException:
                        # If you've been ratelimited, skip the player and notify the console.
                        print("[League] Request rejected for rate limit.")
                    except Exception:
                        # If some other error occours, skip the player
                        print("[League] Request returned an unhandled exception.")
                    else:
                        # Check for level changes
                        if "level" not in db[player]["league"] or r["summonerLevel"] > db[player]["league"]["level"]:
                            # Send the message
                            loop.create_task(send_event(eventmsg=s.league_level_up,
                                                        player=player,
                                                        level=r["summonerLevel"]))
                            # Update database
                            db[player]["league"]["level"] = r["summonerLevel"]
                            f = open("db.json", "w")
                            json.dump(db, f)
                            f.close()
                    finally:
                        # Prevent getting ratelimited by Riot
                        await asyncio.sleep(2)
            print("[League] Level check completed.")
            # Wait for the timeout
            await asyncio.sleep(timeout)
        else:
            await asyncio.sleep(1)

# Every timeout seconds, update player mmr and rank
async def brawlhalla_update_mmr(timeout):
    while True:
        if discord_is_ready:
            print("[Brawlhalla] Starting check for mmr changes...")
            # Update mmr for every player in list
            for player in db:
                if "brawlhalla" in db[player]:
                    try:
                        r = await brawlhalla.get_leaderboard_for(db[player]["brawlhalla"]["username"])
                    except None:
                        print("[Brawlhalla] Request returned an unhandled exception.")
                    else:
                        # Parse the page
                        bs = bs4.BeautifulSoup(r.text, "html.parser")
                        # Divide the page into rows
                        rows = bs.find_all("tr")
                        # Find the row containing the rank
                        for row in rows:
                            # Skip header rows
                            if row.has_attr('id') and row['id'] == "rheader":
                                continue
                            # Check if the row belongs to the correct player
                            # (Brawlhalla searches aren't case sensitive)
                            columns = list(row.children)
                            for column in columns:
                                # Find the player name column
                                if column.has_attr('class') and column['class'][0] == "pnameleft":
                                    # Check if the name matches the parameter
                                    if column.string == db[player]["brawlhalla"]["username"]:
                                        break
                            else:
                                continue
                            # Get the current mmr
                            mmr = int(list(row.children)[7].string)
                            # Compare the mmr with the value saved in the database
                            if mmr != db[player]["brawlhalla"]["mmr"]:
                                # Send a message
                                loop.create_task(send_event(s.brawlhalla_new_mmr, player, mmr=mmr,
                                                            oldmmr=db[player]["brawlhalla"]["mmr"]))
                                # Update database
                                db[player]["brawlhalla"]["mmr"] = mmr
                                f = open("db.json", "w")
                                json.dump(db, f)
                                f.close()
                            break
                    finally:
                        await asyncio.sleep(1)
            print("[Brawlhalla] Request returned an unhandled exception.")
            await asyncio.sleep(timeout)
        else:
            await asyncio.sleep(1)

# Send a new event to both Discord and Telegram
async def send_event(eventmsg: str, player: str, **kwargs):
    # Create arguments dict
    mapping = kwargs.copy()
    mapping["eventmsg"] = None
    # Discord
    # The user id is the player argument; convert that into a mention
    mapping["player"] = "<@" + player + ">"
    # Format the event message
    msg = eventmsg.format(**mapping)
    # Send the message
    loop.create_task(d_client.send_message(d_client.get_channel("213655027842154508"), msg))
    # Telegram
    # Find the matching Telegram username inside the db
    mapping["player"] = "@" + db[player]["telegram"]["username"]
    # Convert the Discord Markdown to Telegram Markdown
    msg = eventmsg.replace("**", "*")
    # Format the event message
    msg = msg.format(**mapping)
    # Send the message
    loop.create_task(telegram.send_message(msg, -2141322))


loop.create_task(overwatch_status_change(600))
print("[Overwatch] Added level up check to the queue.")

loop.create_task(league_rank_change(900))
print("[League] Added rank change check to the queue.")

loop.create_task(league_level_up(900))
print("[League] Added level change check to the queue.")

loop.create_task(brawlhalla_update_mmr(1800))
print("[Brawlhalla] Added mmr change check to the queue.")


try:
    loop.run_until_complete(d_client.start(token))
except KeyboardInterrupt:
    loop.run_until_complete(d_client.logout())
    # cancel all tasks lingering
finally:
    loop.close()
