import os
import importlib
import asyncio
import inspect
import logging
from typing import (
    Coroutine
)
from cronus.plugin import Plugin, PluginTask
from cronus.service import Service
from cronus.event import Event

logger = logging.getLogger("core")

class Cronus():

    def __init__(self) -> None:
        self.plugins : dict[str, Plugin]  = {}
        self._services : dict[str, Service] = {}
        self._loop = asyncio.get_event_loop()
        self._listeners = {}

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def logger(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def start(self) -> None:
        self.loop.run_until_complete(self._start())

    async def _start(self) -> None:
        starters = []
        for _, service in self._services.items():
            starters.append(service.on_start())
        if len(starters) == 0:
            pass
        else:
            print(f"running tasks: {starters}")
            await asyncio.gather(*starters)

    def load_service(self, service):
        self._services[service.name] = service

    def load_plugins(self):
        files = os.listdir("cronus/plugins")
        for file in files:
            if not file.endswith(".py"):
                continue
            if file == "__init__.py":
                continue
            name = file[:-3]
            self._load_plugin(name)

    def load_plugin(self, module: str) -> None:
        self._load_plugin(module.split(".")[-1:][0])

    def _load_plugin(self, name):
        module = f"cronus.plugins.{name}"
        try:
            mtype = importlib.import_module(module)
            mod = importlib.reload(mtype)
            for _, klass in inspect.getmembers(mod, inspect.isclass):
                if (issubclass(klass, Plugin) and klass != Plugin):
                    instance = klass()
                    self.plugins[instance.name] = instance
                    instance.logger.info("Loaded")
        except TypeError:
            logger.error("failed to load plugin %s", module, exc_info=True)


    ## handlers are basically special coroutines
    def _authorize_task(self, plugin: Plugin, task: PluginTask, event: Event):
        account = auth.get_account_by_identity(event.source.name, event.get_identity())
        scopes = set(task.scopes) - set(plugin.auth_scopes)
        if not auth.has_scopes(account, scopes):
            raise auth.NotAuthorizedException()

    async def add_listeners(self, container: None, listeners) -> None:
        if not self._listeners[container]:
            self._listeners[container] = (asyncio.Queue(), listeners)
        else:
            logger.warning("Failed to add listeners to container: Container already exists.")

    async def remove_listeners(self, container: None) -> None:
        # TODO: Stop the running tasks for everything in this event container.
        del self._listeners[container]

    async def dispatch(self, event: Event) -> None:
        tasks = []
        for _, value in self._listeners.items():
            queue, handlers = value
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
