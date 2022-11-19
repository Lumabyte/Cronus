from typing import Any
from discord import Client, Intents
from cronus.core import Service, Cronus


class Discord(Client, Service):
    def __init__(self, cronus: Cronus) -> None:
        self.cronus = cronus
        super().__init__(name="discord", cronus=cronus, intents=Intents.default())

    async def on_create(self) -> None:
        pass

    async def on_start(self):
        await self.start("hmmm")

    async def on_stop(self) -> None:
        await self.close()

    async def on_destroy(self) -> None:
        pass

    def dispatch(self, event: str, /, *args: Any, **kwargs: Any) -> None:
        self.cronus.dispatch("discord", event, *args, **kwargs)
