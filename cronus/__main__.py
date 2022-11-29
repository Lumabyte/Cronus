import logging
from cronus.core import Cronus
from cronus.service import Service
from cronus.services.discord import Discord


class FakeService(Service):

    def __init__(self, cronus: Cronus) -> None:
        super().__init__("fakeservice")
        self._cronus = cronus

    async def on_start(self):
        pass


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-12s %(message)s")


if __name__ == "__main__":
    bot = Cronus()
    bot.load_service(Discord(bot))
    bot.load_plugin("cronus.plugins.test")
    #bot.dispatch(Event(None, "message", "this is some random message"))
    bot.start()
