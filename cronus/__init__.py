import logging
from cronus.core import Cronus

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    bot = Cronus()
    bot.load_services()
    bot.load_plugins()
    bot.start()
