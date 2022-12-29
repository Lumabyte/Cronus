import asyncio
import unittest
import cronus

class TestBot(unittest.IsolatedAsyncioTestCase):    
    async def test_example(self):
        self.assertTrue(True)


class TestApplication(unittest.IsolatedAsyncioTestCase):
    async def test_example(self):
        self.assertTrue(self)


class TestPlugin(unittest.IsolatedAsyncioTestCase):
    async def test_example(self):
        self.assertTrue(self)


class TestEvent(unittest.IsolatedAsyncioTestCase):
    async def test_example(self):
        self.assertTrue(self)

