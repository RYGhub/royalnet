import asyncio
loop = asyncio.get_event_loop()
import aiohttp
import async_timeout

class TelegramError(Exception):
    pass


class Bot:
    def __init__(self, token):
        self.token = token
        self.user_data = None
        self.updates = list()
        self.users = list()
        self.chats = list()
        # Update user_data
        loop.run_until_complete(self.update_bot_data())

    async def update_bot_data(self):
        """Update self.user_data with the latest information from /getMe."""
        data = await self.api_request("getMe")
        self.user_data = User(data)

    async def api_request(self, endpoint, **params):
        """Send a request to the Telegram API at the specified endpoint."""
        # Request timeout is 10 seconds.
        with async_timeout.timeout(10):
            # Create a new session for each request.
            async with aiohttp.ClientSession() as session:
                # Send the request to the Telegram API
                token = self.token
                async with session.request("GET", f"https://api.telegram.org/bot{token}/{endpoint}", params=params) as response:
                    # Check for errors in the request
                    if response.status != 200:
                        raise TelegramError(f"Request returned {response.status} {response.reason}")
                    # Parse the json data as soon it's ready
                    data = await response.json()
                    # Check for errors in the response
                    if not data["ok"]:
                        error = data["description"]
                        raise TelegramError(f"Response returned an error: {error}")
                    # Return a dictionary containing the data
                    return data["result"]

class User:
    def __init__(self, user_dict):
        self.user_id = user_dict["id"]
        self.first_name = user_dict["first_name"]
        if "last_name" in user_dict:
            self.last_name = user_dict["last_name"]
        else:
            self.last_name = None
        if "username" in user_dict:
            self.username = user_dict["username"]
        else:
            self.username = None
