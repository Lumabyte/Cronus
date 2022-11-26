from cronus.plugin import Plugin, command, plugin, handler
from cronus.event import Event

import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-12s %(message)s")


@plugin(name="test", description="A useful test plugin.")
class Test(Plugin):
    @command(
        [
            ("test"),
            ("-a", "--alpha"),
            ("-b", "--bravo"),
            ("-c", "--charlie"),
            ("-d", "--delta"),
        ]
    )
    @handler(service="discord", event="message")
    async def test_command(self, event: Event):
        await asyncio.sleep(5)
        self.logger.info("executed handler test_command: %s", event.data)

    @handler()
    async def test_raw(self, event: Event):
        self.logger.info("executed handler test_raw")

    @handler(service="discord", event="message")
    async def test_discord_message(self, event: Event):
        self.logger.info("executed handler test_discord_message")

    @handler(event="message")
    async def test_none_message(self, event: Event):
        self.logger.info("executed handler test_none_message")
        await asyncio.sleep(5)
        self.logger.info("finished execution")



import asyncio
if __name__ == "__main__":

    async def run():
        test = Test()
        ptask = test.on_event(
            Event(
                "discord",
                "message",
                {"message": "test --alpha -c", "timestamp": 1203910239120, "meta": "asdasdasd"},
            )
        )
        await asyncio.create_task(ptask.handler(), name=ptask.handler.__name__)

    asyncio.run(run())
