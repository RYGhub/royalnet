import os

class MissingTokenError(Exception):
    pass

if "telegram_token" in os.environ:
    telegram_token = os.environ["telegram_token"]
else:
    raise MissingTokenError("telegram_token")

if "discord_token" in os.environ:
    discord_token = os.environ["discord_token"]
else:
    raise MissingTokenError("discord_token")

if "lol_token" in os.environ:
    lol_token = os.environ["lol_token"]
else:
    raise MissingTokenError("lol_token")