import unittest
from unittest.mock import patch
from astralink.adb_client import ADBClient, validate_ip, validate_port

class ValidationTests(unittest.TestCase):
    def test_valid_ip(self):
        self.assertEqual(validate_ip("192.0.2.10"), "192.0.2.10")

    def test_invalid_ip(self):
        with self.assertRaises(ValueError):
            validate_ip("not-an-ip")

    def test_invalid_port(self):
        for port in (0, 65536, "bad"):
            with self.assertRaises(ValueError):
                validate_port(port)

    def test_port_string(self):
        self.assertEqual(validate_port("5555"), 5555)

    def test_devices_parse(self):
        client = ADBClient(adb_path="adb")
        with patch.object(client, "run", return_value=(
            "List of devices attached\nabc123 device product:x model:Pixel\n"
            "def456 unauthorized usb:1-2\n")):
            rows = client.devices()
        self.assertEqual(rows[0]["serial"], "abc123")
        self.assertEqual(rows[0]["state"], "device")
        self.assertEqual(rows[1]["state"], "unauthorized")

if __name__ == "__main__":
    unittest.main()
