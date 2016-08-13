import asyncio
import requests
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
    