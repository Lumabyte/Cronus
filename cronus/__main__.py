import asyncio
import logging
from cronus.services import Discord

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    discord = Discord()
    event_loop = asyncio.get_event_loop()
    event_loop.set_debug(True)
    event_loop.run_until_complete(discord.on_start())
    event_loop.run_forever()
