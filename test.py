import asyncio
import sqlite3


class Stateful:
    """
    Statefuls allow for storing and retrieving of states for a context
    in an async fashion. These states will be stored on disk for the time
    being, 1 state per context

    """

    async def __init__(self) -> None:
        pass

    async def get_state(self) -> any:
        """
        return a state polling through the main event loop or that
        of the highest order asyncio looper
        """
        return None

    async def set_state(self, state: any):
        """
        set the state on the hight order asyncio looper or task.
        """
        return state


class Contextual:
    async def take(self, pattern):
        pass

    async def take_maybe(self, pattern):
        pass

    async def take_every(self, pattern, saga, *args):
        pass

    async def take_latest(self, pattern, saga, *args):
        pass

    async def take_leading(self, pattern, saga, *args):
        pass

    async def put(self, action):
        pass

    async def put_resolve(self, action):
        pass

    async def call(self, fn, *args):
        pass

    # async def call([context, fn], *args): pass

    # async def call([context, fnName], *args): pass

    # async def call({context, fn}, *args): pass

    # async def apply(context, fn, [args]): pass

    # async def cps(fn, *args): pass

    # async def cps([context, fn], *args): pass

    # async def cps({context, fn}, *args): pass

    # async def fork(fn, ...args): pass

    # async def fork([context, fn], ...args): pass

    # async def fork({context, fn}, ...args): pass

    # async def spawn(fn, ...args): pass

    # async def spawn([context, fn], ...args): pass

    # async def join(task): pass

    # async def join([...tasks]): pass

    async def cancel(self, task):
        pass

    async def select(self, selector, *args):
        pass

    async def action_channel(self, pattern, buffer: list):
        pass

    async def flush(self, channel):
        pass

    async def cancelled(self):
        pass

    async def set_context(self, props):
        pass

    async def get_context(self, prop):
        pass

    async def delay(self, ms, value: list):
        pass

    async def throttle(self, ms, pattern, handler, *args):
        pass

    async def debounce(self, ms, pattern, func, *args):
        pass

    async def retry(self, retries, delay, func, args):
        pass

    async def race(self, effects):
        pass

    async def all_parrellel(self, effects):
        pass

    async def all_sequencial(self, effects):
        pass


class Modification:
    """
    A modification is a heavier duty plugin that supports receiving inputs from different
    sources, congests them and then mutates the event to pass on to any plugin that requires
    the modified information.

    Modifications can be composed together.
    """

    def __init__(self) -> None:
        pass


class Plugin(Stateful):
    """
    A plugin is an end-of-line handler repository which runs within the context of a modification
    or root context application.
    """

    def __init__(self) -> None:
        pass


class Source:
    """
    A source is bidirection i/o object that can emit events. Events can also be returned to the
    source via some special raw API on the event or by means of event dispatching.
    """

    def __init__(self) -> None:
        pass

    async def start(self):
        pass


## i want to have func(t) returns t

#
# context(top_level_application_context):
#   context(service):
#       -   context(service_handler)
#   context(modification):
#       -   context(plugin_handler)
#       -   context(plugin_handler)
#       - context(modification_handler)
#       - context(modification_handler)
# lets go with 5 layers
#

# sources <--> modifications <-- plugin_handler

# just_one
# wait_for
# fire_and_forget
# latest_of
## find some workding for hepl create an API for

# functio
# context function ( group for function)
#
# group container of [function,function,function, group containuer, function]
#
## async returns nothing as a leaf


class Application:
    def __init__(self) -> None:
        self.sources = []
        self.modifications = []

    def add_source(self, source):
        self.sources.append(source)
        # at some point be able to add a source
        # while hot running

    def add_modification(self, modification):
        self.modifications.append(modification)

    async def start(self):
        tasks = []
        for source in self.sources:
            tasks.append(source.start())
        await asyncio.gather(*tasks)

    async def dispatch(self, event):
        print(f"dispatching: {event}")
        #for modification in self.modifications:
        #    e = event["event"]
        #    if not e.startswith("modification"):
        #        await asyncio.create_task(modification.on_event(event))


class FakeSource(Source):
    def __init__(self, app, name, delay) -> None:
        self.app = app
        self.name = name
        self.delay = delay

    async def start(self):
        await app.dispatch({"event": self.name})
        await asyncio.sleep(self.delay)
        await self.start()


class FakeModification(Modification):
    def __init__(self, app, name) -> None:
        self.app = app
        self.name = name

    async def on_event(self, event):
        e = event["event"]
        await app.dispatch({ "event", f"{self.name}/{e}"})


class FakePlugin(Plugin):
    def __init__(self, app, name) -> None:
        pass

    def start(self):
        pass


if __name__ == "__main__":
    app = Application()
    source1 = FakeSource(app, "fake1", 1)
    source2 = FakeSource(app, "fake2", 5)
    modification1 = FakeModification(app, "modification")
    plugin1 = FakePlugin(app, "plugin1")
    plugin2 = FakePlugin(app, "plugin2")
    plugin3 = FakePlugin(app, "plugin3")

    app.add_source(source1)
    app.add_source(source2)
    app.add_modification(modification1)
    asyncio.run(app.start())
