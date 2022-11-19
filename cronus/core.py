import os
import importlib
import asyncio
import inspect
import logging

#from cronus.services.discord import Discord

class Event:
    def __init__(self) -> None:
        pass

class Cronus():


    def __init__(self) -> None:
        self.plugins = {}
        self.services = {}
        self.reloader = None
        self.discord = None
        self._loop = asyncio.get_event_loop()

    @property
    def get_looper(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def start(self) -> None:
        #self._loop.run_until_complete(self.discord.on_start())
        self._loop.run_forever()

    def load_services(self):
        pass
        #self.services["discord"] = Discord(self)

    def load_plugins(self):
        p = os.listdir("cronus/plugins")
        for x in p:
            if not (x.endswith(".py")):
                continue
            if x == "__init__.py":
                continue
            name = x[:-3]
            self.load_plugin(name)

    def load_plugin(self, name):
        module = f"cronus.plugins.{name}"
        mtype = importlib.import_module(module)
        mod = importlib.reload(mtype)
        for classname, klass in inspect.getmembers(mod, inspect.isclass):
            if (issubclass(klass, Plugin) and klass != Plugin):
                print(f"classname={classname} klass={klass}")
                self.plugins[name] = klass(self)

    def dispatch(self, source, event, *args, **kwargs):
        print(f"event: {source} {event} {args} {kwargs}")
        print(f"plugins={self.plugins}")
        for name in self.plugins:
            plugin = self.plugins[name]
            print(f"in plugin: {name}")
            for method in dir(plugin):
                print(f"checking method {method} in plugin {plugin}")
                if (callable(getattr(plugin, method))):
                    print(f"method is callable")
                    try:
                        m = getattr(plugin, method)
                        if (m.handler is not None):
                            print(f"method {m} is a handler")
                    except:
                        pass
                else:
                    print(f"method is not callable")



class Lifecycle:
    async def on_create(self) -> None:
        pass

    async def on_start(self) -> None:
        pass

    async def on_stop(self) -> None:
        pass

    async def on_destroy(self) -> None:
        pass


class Service(Lifecycle):
    def __init__(self, cronus: Cronus, name: str) -> None:
        super().__init__()
        self.cronus = cronus
        self.name = name
        self.logger = logging.getLogger(f'service.{self.name}')