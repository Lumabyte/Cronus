import unittest
from cronus import Source


class TestSource(unittest.TestCase):
    def test_create_source(self):
        source = Source("test_name")
        self.assertEqual(source.name, "test_name", "Given name doesn't match actual name")
        self.assertNotEqual(source.logger, None, "Logger can not be None")


if __name__ == "__main__":
    unittest.main()
