from cronus.core import Cronus
from cronus.service import Service
from cronus.event import Event


class ConsoleEvent(Event):

    async def reply(self, *args, **kwargs) -> None:
        self.source.logger.info(f"Output: {args}, {kwargs}")


class Console(Service):

    def __init__(self, cronus: Cronus) -> None:
        super().__init__("console")
        self._cronus = cronus
        self._runner = None

    async def on_start(self):
        pass

    async def on_stop(self) -> None:
        await self._runner.close()

    def dispatch(self, event: str, /, *args: any, **kwargs: any) -> None:
        self._cronus.dispatch(ConsoleEvent(self, event, args, kwargs))
