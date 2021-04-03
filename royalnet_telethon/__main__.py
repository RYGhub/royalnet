# Special imports
from __future__ import annotations
import royalnet.royaltyping as t

# External imports
import logging
import importlib
import click
import asyncio
import royalnet.engineer as engi

# Internal imports
from .pda import TelethonPDA

# Special global objects
log = logging.getLogger(__name__)


# Code
@click.command()
@click.option("-p", "--pack", "packs", multiple=True)
@click.option("-i", "--api-id", "api_id", required=True, type=int)
@click.option("-h", "--api-hash", "api_hash", required=True)
@click.option("-t", "--token", "token", required=True)
@click.option("-u", "--username", "username", required=True)
def main(packs: t.List[str], token: str, api_id: int, api_hash: str, username: str):
    log.debug("Creating PDA...")
    pda = TelethonPDA(tg_api_id=api_id, tg_api_hash=api_hash, bot_username=username)

    for pack in packs:
        log.debug(f"Importing module: {pack!r}")
        try:
            pack = importlib.import_module(pack)
        except ImportError as e:
            log.error(f"Skipping {pack!r}: {e!r}")
            continue

        for attribute in dir(pack):
            log.debug(f"Getting attribute: {attribute!r}")
            value = pack.__getattribute__(attribute)
            log.debug(f"Attribute is: {value!r}")

            if isinstance(value, engi.PartialCommand):
                log.debug(f"Attribute is a PartialCommand, registering it as: {value.f.__name__!r}")
                pda.register_partial(part=value, names=[value.f.__name__])

            elif isinstance(value, engi.Conversation):
                log.debug(f"Attribute is a Conversation, registering it...")
                pda.register_conversation(conv=value)

    log.debug("Getting event loop...")
    loop = asyncio.get_event_loop()
    log.debug(f"Event loop is: {loop!r}")

    log.debug("Running the PDA until interrupted...")
    try:
        loop.run_until_complete(pda.run(bot_token=token))
    except KeyboardInterrupt:
        log.debug("Got an interrupt, shutting down...")
        exit(0)

    log.fatal("PDA stopped unexpectedly, shutting down...")
    exit(1)


if __name__ == "__main__":
    main()
