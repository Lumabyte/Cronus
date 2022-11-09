from cronus.core import Plugin, Event, discord


class Weather(Plugin):
    def __init__(self, chronus) -> None:
        super().__init__(chronus, "weather")

    @discord("socket_event_type")
    async def s_1(self, event: Event):
        self.logger.info("s1: %s", event)

    @discord("guild_available")
    async def s_2(self, event: Event):
        self.logger.info("s2: %s", event)

    @discord("ready")
    async def s_3(self, event: Event):
        self.logger.info("s3: %s", event)
