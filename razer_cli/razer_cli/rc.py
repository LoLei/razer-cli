from argparse import Namespace

from openrazer.client import DeviceManager

from razer_cli.razer_cli import util
from razer_cli.razer_cli.handler.brightness_handler import BrightnessHandler
from razer_cli.razer_cli.handler.color_effect_handler import ColorEffectHandler
from razer_cli.razer_cli.handler.version_handler import VersionHandler
from razer_cli.razer_cli.lister.lister import list_devices
from razer_cli.razer_cli.setter.battery_setter import set_battery
from razer_cli.razer_cli.setter.dpi_setter import set_dpi
from razer_cli.razer_cli.setter.poll_rate_setter import set_poll_rate


class RazerCli:
    def __init__(self, device_manager: DeviceManager, args: Namespace, version: str):
        self.device_manager = device_manager
        self.args = args
        self.version = version
        self.color_effect_handler = ColorEffectHandler(device_manager, args)
        self.brightness_handler = BrightnessHandler(device_manager, args)
        self.version_handler = VersionHandler(device_manager, args, version)

    def run(self):
        self.device_manager.sync_effects = self.args.sync

        if self.args.automatic or self.args.effect or self.args.color:
            self.color_effect_handler.handle()

        if self.args.restore:
            util.load_settings_from_file(self.args.verbose)

        if self.args.dpi:
            set_dpi(self.device_manager, self.args)

        if self.args.poll:
            set_poll_rate(self.device_manager, self.args)

        if self.args.battery:
            set_battery(self.device_manager, self.args)

        if self.args.brightness:
            self.brightness_handler.handle()

        if self.args.list_devices or self.args.list_devices_long or self.args.list_devices_short:
            list_devices(self.device_manager, self.args)

        if self.args.version:
            self.version_handler.handle()
