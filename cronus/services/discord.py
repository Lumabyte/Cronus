from discord import Client, Intents
from cronus.core import Service, Cronus
from cronus.event import Event


class DiscordEvent(Event):

    async def reply(self, message, **kwargs) -> None:
        await self["raw_event"].channel.send(message)


class Discord(Client, Service):
    def __init__(self, cronus: Cronus) -> None:
        self.cronus = cronus
        super().__init__(name="discord", cronus=cronus, intents=Intents.default())

    async def on_start(self):
        await self.start("hmmm")

    async def on_stop(self) -> None:
        await self.close()

    def dispatch(self, event: str, /, *args: any, **kwargs: any) -> None:
        self.cronus.dispatch(DiscordEvent(self, event, args, kwargs))
