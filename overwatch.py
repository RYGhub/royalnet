import asyncio
import requests
import strings as s
loop = asyncio.get_event_loop()


class NotFoundException(Exception):
    pass

# Get player data
async def get_player_data(platform: str, region: str, battletag: str, **kwargs):
    print("[Overwatch] Getting player info for: {platform} {region} {battletag}".format(platform=platform,
                                                                                        region=region,
                                                                                        battletag=battletag))
    # Unofficial API requires - for discriminator numbers
    battletag = battletag.replace("#", "-")
    # GET the json unofficial API response
    r = await loop.run_in_executor(None, requests.get,
                                   'https://api.lootbox.eu/{platform}/{region}/{battletag}/profile'.format(**locals()))
    # Ensure the request is successful
    if r.status_code == 200:
        # Parse json and check for the status code inside the response
        pj = r.json()
        if "statusCode" in pj:
            if pj["statusCode"] == 404:
                raise NotFoundException("Player not found.")
            else:
                raise Exception("Unhandled API response.")
        else:
            # Success!
            return pj
    else:
        raise Exception("Unhandled API response.")


# Convert rank to a medal
def rank_to_medal(rank):
    # Unranked
    if int(rank) == 0:
        return s.overwatch_medal_list[0]
    # Bronze
    elif int(rank) < 1500:
        return s.overwatch_medal_list[1]
    # Silver
    elif int(rank) < 2000:
        return s.overwatch_medal_list[2]
    # Gold
    elif int(rank) < 2500:
        return s.overwatch_medal_list[3]
    # Platinum
    elif int(rank) < 3000:
        return s.overwatch_medal_list[4]
    # Diamond
    elif int(rank) < 3500:
        return s.overwatch_medal_list[5]
    # Master
    elif int(rank) < 4000:
        return s.overwatch_medal_list[6]
    # Grandmaster
    elif int(rank) <= 5000:
        return s.overwatch_medal_list[7]
    # ???
    else:
        raise NotFoundException("The medal does not exist.")

# Convert an url to a medal
def url_to_medal(rank: str):
    # Bronze
    if rank == "https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-1.png":
        return s.overwatch_medal_list[1]
    # Silver
    elif rank == "https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-2.png":
        return s.overwatch_medal_list[2]
    # Gold
    elif rank == "https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-3.png":
        return s.overwatch_medal_list[3]
    # Platinum
    elif rank == "https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-4.png":
        return s.overwatch_medal_list[4]
    # Diamond
    elif rank == "https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-5.png":
        return s.overwatch_medal_list[5]
    # Master
    elif rank == "https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-6.png":
        return s.overwatch_medal_list[6]
    # Grandmaster
    elif rank == "https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-7.png":
        return s.overwatch_medal_list[7]
    else:
        raise NotFoundException("The medal does not exist.")

def format_rankchange(rankchange: int):
    if rankchange > 0:
        return "+" + str(rankchange)
    else:
        return str(rankchange)