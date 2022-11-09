from cronus.core import Plugin, handler


class Crypto(Plugin):
    def __init__(self, chronus) -> None:
        super().__init__(chronus, "crypto")

    @handler("discord", "message")
    async def tracker_create(self):
        self.logger.info("tracker_create")

    async def tracker_add_wallet(self):
        pass

    async def tracker_get_summary(self):
        pass
