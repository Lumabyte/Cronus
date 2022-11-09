import os
import importlib
import inspect
import logging

class Event:
    def __init__(self) -> None:
        pass

class Cronus():
    def __init__(self) -> None:
        self.plugins = {}
        self.services = {}
        self.reloader = None
        self.discord = None

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


class Plugin(Lifecycle):
    def __new__(cls: type[Self]) -> Self:
        list = "_Plugin_event_handlers"

        if not hasattr(cls, list):
            setattr(cls, list, [])
        list = getattr(cls. list)

        return super().__new__()

    def __init__(self, cronus: Cronus, name: str) -> None:
        super().__init__()
        self.cronus = cronus
        self.name = name
        self.logger = logging.getLogger(f'plugin.{self.name}')

    def get_state():
        pass

    def set_state():
        pass

def plugin(version: str, author: str, ):
    def wrapper(cls):
        cls.version="",
        cls.author="",
        cls.meta=""
        return cls
    return wrapper

def handler(service: str, event: str):
    def wrapper(function):
        function.service = service
        function.event = event
        return function
    return wrapper


def discord(event: str):
    def wrapper(function):
        function.service = "discord"
        function.event = event
        return function
    return wrapper


def http(event: str):
    def wrapper(function):
        function.service = "http"
        function.event = event
        return function
    return wrapper
