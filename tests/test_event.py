import unittest
from cronus.event import Event


class TestEvent(unittest.TestCase):
    def test_create_event(self):
        event = Event("test", {})
        self.assertEqual(event.event, "test", "event name mismatch")
        self.assertEqual(event.data, {}, "incorrect data mismatch")


if __name__ == "__main__":
    unittest.main()
