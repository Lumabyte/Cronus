import logging
from cronus.core import Cronus
from cronus.sources.discord import Discord


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-12s %(message)s")


if __name__ == "__main__":
    bot = Cronus()
    bot.load_service(Discord(bot))
    bot.load_plugin("cronus.plugins.test")
    bot.start()
