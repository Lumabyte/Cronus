from cronus.plugin import Plugin, command, plugin, handler
from cronus.event import Event


@plugin(name="test", description="A useful test plugin.")
class Test(Plugin):

    @command([
        ('-a', '--alpha'),
        ('-b', '--bravo'),
        ('-c', '--charlie'),
        ('-d', '--delta'),
    ])
    async def test_command(self, event: Event):
        pass

    @handler()
    async def test_raw(self, event: Event):
        pass
