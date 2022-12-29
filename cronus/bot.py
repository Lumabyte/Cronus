import asyncio
import logging
from typing import Coroutine

logger = logging.getLogger("core")


class Event:
    def __init__(self, source, name) -> None:
        self._source = source
        self._name = name

    @property
    def source(self) -> str:
        return self._source

    @property
    def name(self) -> str:
        return self._name


class Source:
    async def setup(self, application):
        self.application = application

    async def start(self):
        pass

    async def stop(self):
        pass

    def emit(self, name):
        self.application.dispatch(Event(
            source=self,
            name=name
        ))


class Plugin:
    async def setup(self):
        pass


class Service:
    async def setup(self):
        pass


class ClickSource(Source):

    ticks = 0
    max_ticks = 10

    async def start(self):
        print(f"creating click task")
        await asyncio.create_task(self._create_clock_task())
        print(f"finished creating click task")

    async def _create_clock_task(self):
        print("running click task")
        while self.ticks <= self.max_ticks:
            print("clock click ticked")
            await asyncio.sleep(1)
            self.emit("click")
            self.ticks += 1


class ClockSource(Source):

    tocks = 0
    max_tocks = 5

    async def start(self):
        print(f"creating clock task")
        await asyncio.create_task(self._create_clock_task())
        print(f"finished creating clock task")

    async def _create_clock_task(self):
        print("running clock task")
        while self.tocks <= self.max_tocks:
            print("clock task ticked")
            await asyncio.sleep(1)
            self.emit("clock")
            self.tocks += 1


class Application:
    def __init__(self) -> None:
        self.logger: logging.Logger = logger.getChild("application")
        self._plugins: list[tuple[asyncio.Queue, Plugin]] = []
        self._services: dict[str, Source] = {}
        self._sources: dict[str, Source] = {}

    @property
    def plugins(self):
        return self._plugins

    @property
    def services(self):
        return self._services

    @property
    def sources(self):
        return self._sources

    async def add_services(self, services: list[Service]) -> None:
        for service in services:
            name = service.__class__.__name__
            if name in self.services:
                logger.warning(
                    "Failed to load service because an identical service '%s' exists", name)
                continue
            try:
                await service.setup(self)
                self._services[name] = service
            except:  # pylint: disable=bare-except
                logger.error("Failed to load service %s", name, exc_info=True)

    async def add_sources(self, sources: list[Source]) -> None:
        for source in sources:
            name = source.__class__.__name__
            if name in self.sources:
                logger.warning(
                    "Failed to load source because an identical source '%s' exists", name)
                continue
            try:
                await source.setup(self)
                self._sources[name] = source
            except:  # pylint: disable=bare-except
                logger.error("Failed to load source", exc_info=True)

    async def add_plugins(self, plugins: list[Plugin]) -> None:
        for plugin in plugins:
            try:
                await plugin.setup(self)
                self._plugins.append(plugin)
            except:  # pylint: disable=bare-except
                logger.error("Failed to load plugin", exc_info=True)

    async def start(self):
        print(f"starting bot")
        runners = []
        for _, source in self.sources.items():
            task = asyncio.create_task(source.start())
            runners.append(task)
            print(f"added task {task}")
        print(f"gathering all runners")
        await asyncio.gather(*runners)

    def run(self):
        asyncio.run(self.start())

    def dispatch(self, event: Event) -> None:
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
            except:  # pylint: disable=bare-except
                logger.error("Failed to run event handler", exc_info=True)
        queue.task_done()


class Bot(Application):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger.getChild("bot")


async def setup():
    bot = Bot()
    await bot.add_sources([ClockSource(), ClickSource()])
    await bot.start()


# this is just a place-holder to quickly run this script.
if __name__ == "__main__":
    asyncio.run(setup())
