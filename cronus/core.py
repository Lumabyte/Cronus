import os
import importlib
import asyncio
import inspect
import logging

from cronus.db import Session
from cronus.plugin import Plugin, PluginTask
from cronus.event import Event

logger = logging.getLogger("core")

class Cronus():

    def __init__(self) -> None:
        self.plugins : dict[str, Plugin]  = {}
        self.services = {}
        self._loop = asyncio.get_event_loop()
        self._session = 

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def logger(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def start(self) -> None:
        self._loop.run_forever()

    def load_services(self):
        pass

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
                self._loop.create_task(task, name=f'cronus.core.dispatcher: {plugin.name}/{event.name}')
            except Exception:
                logger.error("failed to run %s event task for plugin %s", event.name, name)

    ## handlers are basically special coroutines
    def _handler_authorizer(self, task: PluginTask):
        ## no one can access any method unless scopes allow for it.
        ## scope "*" means any scope matching the pattern
        # - get the current user executing the event
        # - get their permissions
        # if the user permission scopes satisfy the required scopes, proceed.
        # - if not, raise an exception to propogate upstream to the source service.
        pass
