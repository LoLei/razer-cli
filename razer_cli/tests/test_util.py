"""Test util functions"""
import json
import os.path
import tempfile
import unittest
# from openrazer.client import DeviceManager
from pathlib import Path
from unittest.mock import MagicMock, patch

from razer_cli.razer_cli import settings, util


class TestUtil(unittest.TestCase):
    """Test the util functions."""

    def test_write_settings_to_file(self):
        """> Test if cache file writing works"""

        with tempfile.TemporaryDirectory() as tmp_home:
            with patch("razer_cli.razer_cli.util.os.path.expanduser",
                       return_value=tmp_home):
                # Build file path
                dir_name = settings.CACHE_DIR
                file_name = settings.CACHE_FILE
                path_and_file = os.path.join(tmp_home, dir_name, file_name)

                # Save random device settings to cache
                device = MagicMock()
                device.name = "test_device"
                device.serial = "test_serial"
                util.write_settings_to_file(device, dpi="1234")
                util.write_settings_to_file(device, effect=["multicolor"])

                # Check if file has been written
                self.assertTrue(os.path.isfile(path_and_file))

                # Check contents
                data = json.loads(Path(path_and_file).read_text())[0]
                self.assertEqual(data["device_name"], "test_device")
                self.assertEqual(data["serial"], "test_serial")
                self.assertEqual(data["dpi"], "1234")
                self.assertEqual(data["effect"], ["multicolor"])

    def test_hex_to_decimal(self):
        """> Test if hex converting works"""

        red, green, blue = util.hex_to_decimal("3399ff")

        self.assertEqual(red, 51)
        self.assertEqual(green, 153)
        self.assertEqual(blue, 255)

    def test_random_color(self):
        """> Test if random color works"""

        red, green, blue = util.get_random_color_rgb()

        self.assertTrue(0 <= red <= 255)
        self.assertTrue(0 <= green <= 255)
        self.assertTrue(0 <= blue <= 255)

    def test_x_color(self) -> None:
        color = util.get_x_color()
        self.assertEqual(3, len(color))

    def test_x_colors(self) -> None:
        colors = util.get_x_colors()
        self.assertEqual(16, len(colors))


if __name__ == "__main__":
    unittest.main()
