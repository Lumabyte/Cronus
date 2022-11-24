import logging
from cronus.core import Cronus
from cronus.event import Event
from cronus.service import Service

class FakeService(Service):
    def __init__(self) -> None:
        super().__init__("FakeService")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(message)s')

if __name__ == "__main__":
    bot = Cronus()
    bot.load_services()
    bot.load_plugin("cronus.plugins.test")

    fake = FakeService()
    bot.dispatch(Event(fake, "test"))
    bot.start()
