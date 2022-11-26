import os
import importlib
import asyncio
import inspect
import logging
from cronus.plugin import Plugin, PluginTask
from cronus.service import Service
from cronus.event import Event
from cronus import auth

logger = logging.getLogger("core")

class Cronus():

    def __init__(self) -> None:
        self.plugins : dict[str, Plugin]  = {}
        self._services : dict[str, Service] = {}
        self._loop = asyncio.get_event_loop()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def logger(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def start(self) -> None:
        self._loop.run_until_complete(self._start())
        #asyncio.run(self._start())

    async def _start(self) -> None:
        starters = []
        for _, service in self._services.items():
            starters.append(await service.on_start())
        if len(starters) == 0:
            pass
        else:
            await asyncio.gather(starters[0])

    def load_service(self, service):
        self._services["derp"] = service

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
                    instance.logger().info("Loaded")
        except Exception:
            logger.error("failed to load plugin %s", module)

    ## Handle auth stuff here rather than in the plugin itself.
    def dispatch(self, event: Event) -> None:
        logger.info("dispatching event: %s", event.name)
        for name, plugin in self.plugins.items():
            try:
                task = plugin.on_event(event)

                self._authorize_task(plugin, task, event)

                self._loop.create_task(task, name=f'cronus.core.dispatcher: {plugin.name}/{event.name}')
            except Exception:
                logger.error("failed to run %s event task for plugin %s", event.name, name)

    ## handlers are basically special coroutines
    def _authorize_task(self, plugin: Plugin, task: PluginTask, event: Event):
        account = auth.get_account_by_identity(event.source.name, event.get_identity())
        scopes = set(task.scopes) - set(plugin.auth_scopes)
        if not auth.has_scopes(account, scopes):
            raise auth.NotAuthorizedException()
