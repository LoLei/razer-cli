from argparse import Namespace

from openrazer.client import DeviceManager

from razer_cli.razer_cli import util
from razer_cli.razer_cli.handler.brightness_handler import BrightnessHandler
from razer_cli.razer_cli.handler.color_effect_handler import ColorEffectHandler
from razer_cli.razer_cli.handler.version_handler import VersionHandler
from razer_cli.razer_cli.lister.device_lister import DeviceLister
from razer_cli.razer_cli.setter.battery_setter import BatterySetter
from razer_cli.razer_cli.setter.brightness_setter import BrightnessSetter
from razer_cli.razer_cli.setter.color_effect_setter import ColorEffectSetter
from razer_cli.razer_cli.setter.dpi_setter import DpiSetter
from razer_cli.razer_cli.setter.poll_rate_setter import PollRateSetter


class RazerCli:
    def __init__(self, device_manager: DeviceManager, args: Namespace, version: str):
        self.device_manager = device_manager
        self.args = args
        self.version = version
        self.color_effect_handler = ColorEffectHandler(device_manager, args,
                                                       setter=ColorEffectSetter(device_manager, args))
        self.brightness_handler = BrightnessHandler(device_manager, args, setter=BrightnessSetter(device_manager, args))
        self.version_handler = VersionHandler(device_manager, args, version=version)
        self.device_lister = DeviceLister(device_manager, args)
        self.dpi_setter = DpiSetter(device_manager, args)
        self.poll_rater_setter = PollRateSetter(device_manager, args)
        self.battery_setter = BatterySetter(device_manager, args)

    def run(self):
        self.device_manager.sync_effects = self.args.sync

        if self.args.automatic or self.args.effect or self.args.color:
            self.color_effect_handler.handle()

        if self.args.restore:
            util.load_settings_from_file(self.args.verbose)

        if self.args.dpi:
            self.dpi_setter.set()

        if self.args.poll:
            self.poll_rater_setter.set()

        if self.args.battery:
            self.battery_setter.set()

        if self.args.brightness:
            self.brightness_handler.handle()

        if self.args.list_devices or self.args.list_devices_long or self.args.list_devices_short:
            self.device_lister.list()

        if self.args.version:
            self.version_handler.handle()
