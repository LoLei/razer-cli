from argparse import Namespace

from openrazer.client import DeviceManager

from razer_cli.razer_cli import util
from razer_cli.razer_cli.handler.brightness_handler import BrightnessHandler
from razer_cli.razer_cli.handler.color_effect_handler import ColorEffectHandler
from razer_cli.razer_cli.handler.handler import Handler
from razer_cli.razer_cli.handler.version_handler import VersionHandler
from razer_cli.razer_cli.lister.device_lister import DeviceLister
from razer_cli.razer_cli.lister.lister import Lister
from razer_cli.razer_cli.setter.battery_setter import BatterySetter
from razer_cli.razer_cli.setter.brightness_setter import BrightnessSetter
from razer_cli.razer_cli.setter.color_effect_setter import ColorEffectSetter
from razer_cli.razer_cli.setter.dpi_setter import DpiSetter
from razer_cli.razer_cli.setter.poll_rate_setter import PollRateSetter
from razer_cli.razer_cli.setter.setter import Setter


class RazerCli:
    def __init__(self, device_manager: DeviceManager, args: Namespace, version: str,
                 color_effect_handler: Handler, brightness_handler: Handler, version_handler: Handler,
                 device_lister: Lister,
                 dpi_setter: Setter, poll_rater_setter: Setter, battery_setter: Setter) -> None:
        self.device_manager = device_manager
        self.args = args
        self.version = version
        self.color_effect_handler = color_effect_handler
        self.brightness_handler = brightness_handler
        self.version_handler = version_handler
        self.device_lister = device_lister
        self.dpi_setter = dpi_setter
        self.poll_rater_setter = poll_rater_setter
        self.battery_setter = battery_setter

    @staticmethod
    def init_create(device_manager: DeviceManager, args: Namespace, version: str) -> 'RazerCli':
        """ Factory method to have dependency injection available on the constructor """
        color_effect_handler = ColorEffectHandler(device_manager, args, setter=ColorEffectSetter(device_manager, args))
        brightness_handler = BrightnessHandler(device_manager, args, setter=BrightnessSetter(device_manager, args))
        version_handler = VersionHandler(device_manager, args, version=version)
        device_lister = DeviceLister(device_manager, args)
        dpi_setter = DpiSetter(device_manager, args)
        poll_rater_setter = PollRateSetter(device_manager, args)
        battery_setter = BatterySetter(device_manager, args)
        return RazerCli(device_manager, args, version,
                        color_effect_handler, brightness_handler, version_handler,
                        device_lister,
                        dpi_setter, poll_rater_setter, battery_setter)

    def run(self) -> None:
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
