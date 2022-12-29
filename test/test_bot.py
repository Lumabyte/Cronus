import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from cronus.bot import Application, Plugin, Source, Service


class FakeSource(Source):
    pass

class FakePlugin(Plugin):
    pass

class FakeService(Service):
    pass


class TestBot(IsolatedAsyncioTestCase):
    async def test_example(self):
        self.assertTrue(True)


class TestApplication(IsolatedAsyncioTestCase):
    async def test_init_empty_plugins(self):
        app = Application()
        self.assertEqual(len(app.plugins), 0)

    async def test_init_empty_sources(self):
        app = Application()
        self.assertEqual(len(app.sources), 0)

    async def test_init_empty_services(self):
        app = Application()
        self.assertEqual(len(app.services), 0)

    async def test_add_plugins(self):
        app = Application()
        await app.add_plugins([ FakePlugin(), FakePlugin() ])
        self.assertEqual(len(app.plugins), 2)

    async def test_add_sources(self):
        app = Application()
        await app.add_sources([ FakeSource() ])
        self.assertEqual(len(app.sources), 1)

    async def test_add_sources_no_duplicates(self):
        app = Application()
        await app.add_sources([ FakeSource(), FakeSource() ])
        self.assertEqual(len(app.sources), 1)

    async def test_add_services(self):
        app = Application()
        await app.add_services([ FakeService() ])
        self.assertEqual(len(app.services), 1)

    async def test_add_services_no_duplicates(self):
        app = Application()
        await app.add_services([ FakeService(), FakeService() ])
        self.assertEqual(len(app.services), 1)

class TestPlugin(IsolatedAsyncioTestCase):
    async def test_example(self):
        self.assertTrue(self)


class TestEvent(IsolatedAsyncioTestCase):
    async def test_example(self):
        self.assertTrue(self)
