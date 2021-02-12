"""Test util functions"""
import json
import os.path
import shutil
import unittest
# from openrazer.client import DeviceManager
from pathlib import Path
from unittest.mock import MagicMock

from razer_cli.razer_cli import settings, util


class TestUtil(unittest.TestCase):
    """Test the util functions."""

    def test_write_settings_to_file(self):
        """> Test if cache file writing works"""

        # Build file path
        home_dir = os.path.expanduser("~")
        dir_name = settings.CACHE_DIR
        file_name = settings.CACHE_FILE
        path_and_file = os.path.join(home_dir, dir_name, file_name)

        # Backup original file if this is running locally
        if Path(path_and_file).exists():
            shutil.copyfile(path_and_file, path_and_file + "_backup")

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

        # Restore original file
        if Path(path_and_file + "_backup").exists():
            shutil.copyfile(path_and_file + "_backup", path_and_file)
            Path(path_and_file + "_backup").unlink()

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


if __name__ == "__main__":
    unittest.main()
