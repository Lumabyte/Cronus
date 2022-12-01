import asyncio
import logging
from typing import Coroutine
from cronus import Plugin, Source, Event, Service

logger = logging.getLogger("core")


class Application:
    def __init__(self) -> None:
        self.logger: logging.Logger = logger.getChild("application")
        self.plugins: list[tuple[asyncio.Queue, Plugin]] = []

    async def add_services(self, services: list[Service]) -> None:
        pass

    async def add_sources(self, plugins: list[Source]) -> None:
        pass

    async def add_plugins(self, plugins: list[Plugin]) -> None:
        pass

    async def start(self):
        pass

    async def run(self):
        asyncio.run(self.start())

    async def dispatch(self, event: Event) -> None:
        tasks = []
        for queue, plugin in self.plugins:
            handlers = plugin.get_event_handlers()
            self._queue_event(queue, event)
            task = self._queue_runnable_tasks(queue, handlers)
            tasks.append(task)
        await asyncio.gather(*tasks)

    def _queue_event(self, queue: asyncio.Queue, event: Event):
        queue.put_nowait(event)

    def _queue_runnable_tasks(self, queue: asyncio.Queue, handlers: Coroutine):
        return asyncio.create_task(self._run_ordered_task(queue, handlers))

    async def _run_ordered_task(self, queue: asyncio.Queue, handlers: list[Coroutine]):
        event = await queue.get()
        for handler in handlers:
            try:
                await handler(event)
            except: # pylint: disable=bare-except
                logger.error("Failed to run event handler", exc_info=True)
        queue.task_done()


class Bot(Application):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger.getChild("bot")


if __name__ == "__main__":
    bot = Bot()
    bot.start()
