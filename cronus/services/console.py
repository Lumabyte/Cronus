import sys
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

    async def on_start(self):
        loop = self._cronus.loop
        await loop.run_in_executor(None, self._std_in)

    async def on_stop(self) -> None:
        pass

    def dispatch(self, event: str, /, *args: any, **kwargs: any) -> None:
        self._cronus.dispatch(ConsoleEvent(self, event, args, kwargs))

    def _std_in(self):
        line = sys.stdin.readline
        self.logger.info("read line: %s", line)
