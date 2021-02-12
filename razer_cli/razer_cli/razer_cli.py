#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lorenz Leitner"
__version__ = "2.0.0"
__license__ = "GPL-3.0"

import argparse
import sys

from openrazer.client import DeviceManager

from razer_cli.razer_cli import util
from razer_cli.razer_cli.listing.lister import list_devices
from razer_cli.razer_cli.parsing.argument_parser import read_args
from razer_cli.razer_cli.parsing.color_parser import parse_color
from razer_cli.razer_cli.parsing.zone_parser import parse_zones
from razer_cli.razer_cli.setting.battery_setter import set_battery
from razer_cli.razer_cli.setting.brightness_setter import set_brightness
from razer_cli.razer_cli.setting.dpi_setter import set_dpi
from razer_cli.razer_cli.setting.effect_setter import set_effect_to_all_devices
from razer_cli.razer_cli.setting.poll_rate_setter import set_poll_rate

args: argparse.Namespace


def handle_colors_and_effects(device_manager):
    color = []
    if args.color:
        color = parse_color(args.color, args)
    elif args.automatic:
        color = [util.get_x_color(args.verbose)]
    zones = parse_zones(args.zones)
    if not args.effect:
        effects = ['static']
        if args.automatic and not args.brightness and len(zones) == 1:
            effects.append('brightness')
    else:
        effects = args.effect

    stop = len(zones)
    if len(effects) == 1 and stop > 1:
        while len(effects) < stop:
            effects.append(effects[0])
    elif stop == 1 and len(effects) > 1:
        stop = len(effects)
        while len(zones) < stop:
            zones.append([*zones[0]])

    set_effect_to_all_devices(device_manager, effects, color, zones, args)


def handle_brightness(device_manager):
    i = len(args.brightness)
    if i == 1 and args.brightness[0].isnumeric():
        args.brightness = {"all": args.brightness[0]}
        set_brightness(device_manager, args)
    elif i % 2 == 0:
        # Even number of arguments
        brightness = {}
        i = i - 1
        while i > -1:
            name = args.brightness[i - 1]
            value = args.brightness[i]
            if args.brightness[i].isnumeric():
                brightness[name] = value
            else:
                print('Warning:', value, 'is not a number for',
                      name, '[Skipping]')
            i = i - 2
        args.brightness = brightness
        set_brightness(device_manager, args)
    else:
        print("Invalid brightness input, see `razer-cli --manual brightness'")


def handle_version(device_manager):
    print("razer-cli:", __version__)
    print("   Installed in:",
          util.os.path.dirname(util.os.path.realpath(__file__)))
    print("python3-openrazer:", device_manager.version)
    print("openrazer-daemon:", device_manager.daemon_version)
    print("Python:", '.'.join([str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)]))


def main():
    """ Main entry point of the app """
    global args
    args = read_args(sys.argv[1:])

    if args.manual is not None:
        return util.print_manual(args.manual)

    # Create a DeviceManager. This is used to get specific devices
    device_manager = DeviceManager()

    # Disable daemon effect syncing.
    # Without this, the daemon will try to set the lighting effect to every
    # device.
    device_manager.sync_effects = args.sync

    if args.automatic or args.effect or args.color:
        handle_colors_and_effects(device_manager)

    if args.restore:
        util.load_settings_from_file(args.verbose)

    if args.dpi:
        set_dpi(device_manager, args)

    if args.poll:
        set_poll_rate(device_manager, args)

    if args.battery:
        set_battery(device_manager, args)

    if args.brightness:
        handle_brightness(device_manager)

    if args.list_devices or args.list_devices_long or args.list_devices_short:
        list_devices(device_manager, args)

    if args.version:
        handle_version(device_manager)


if __name__ == "__main__":
    """ This is executed when run from the command line - obsolete """

    main()
