import asyncio
import requests


class NotFoundException(Exception):
    pass


class NoRankedGamesCompletedException(Exception):
    pass


loop = asyncio.get_event_loop()

# Load League of Legends API key from the leaguetoken.txt file
file = open("leaguetoken.txt", "r")
token = file.read()
file.close()

ranklist = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'CHALLENGER']
roman = ['I', 'II', 'III', 'IV', 'V']


# Get player rank info
async def get_player_rank(region: str, summonerid: int, **kwargs):
    # GET the json unofficial API response
    r = await loop.run_in_executor(None, requests.get,
                                   'https://{region}.api.pvp.net/api/lol/{region}/v2.5/league/by-summoner/{summonerid}'
                                   '/entry?api_key={token}'.format(region=region, summonerid=summonerid, token=token))
    # Ensure the request is successful
    if r.status_code == 200:
        if len(r.json()[str(summonerid)]) > 0:
            return r.json()[str(summonerid)][0]
        else:
            raise NoRankedGamesCompletedException("This player hasn't completed any ranked games.")
    elif r.status_code == 404:
        raise NotFoundException("Player not found.")
    else:
        raise Exception("Unhandled API response.")
