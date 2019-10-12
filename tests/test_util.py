"""Test util functions"""

import unittest
import os.path
# from openrazer.client import DeviceManager

from razer_cli import settings
from razer_cli import util


class TestUtil(unittest.TestCase):
    """Test the util functions."""

    def disabled_test_write_settings_to_file(self):
        """> Test if cache file writing works"""

        # Save random device settings to cache
        # device_manager = DeviceManager()
        # util.write_settings_to_file(device_manager.devices[0], dpi="1234")

        # Check if file has been written - Could be extended to check whether
        # settings have been written correctly as well
        home_dir = os.path.expanduser("~")
        dir_name = settings.CACHE_DIR
        file_name = settings.CACHE_FILE
        path_and_file = os.path.join(home_dir, dir_name, file_name)
        result = os.path.isfile(path_and_file)

        self.assertEqual(result, True)

    def test_hex_to_decimal(self):
        """> Test if hex converting works"""

        red, green, blue = util.hex_to_decimal("3399ff")

        self.assertEqual(red, 51)
        self.assertEqual(green, 153)
        self.assertEqual(blue, 255)


if __name__ == "__main__":
    unittest.main()
