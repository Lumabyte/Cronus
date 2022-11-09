import os
import inspect
import importlib
import asyncio
import logging

from cronus.core import Cronus
from cronus.services import Discord


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    bot = Cronus()
    bot.load_plugins()
    bot.discord = Discord(bot)
    print(bot.plugins) # Works
    print(bot.discord) # None?
    event_loop = asyncio.get_event_loop()
    event_loop.set_debug(True)
    event_loop.run_until_complete(bot.discord.on_start())
    event_loop.run_forever()
