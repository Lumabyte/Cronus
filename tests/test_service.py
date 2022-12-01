import unittest
from cronus import Service


class TestService(unittest.TestCase):
    def test_create_service(self):
        service = Service("test_name")
        self.assertEqual(service.name, "test_name", "Given name doesn't match actual name")
        self.assertNotEqual(service.logger, None, "Logger can not be None")


if __name__ == "__main__":
    unittest.main()
