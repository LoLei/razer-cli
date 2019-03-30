#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lorenz Leitner"
__version__ = "0.1.0"
__license__ = "MIT" # TODO: Change

import subprocess, sys
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import argparse

def hex_to_decimal(hex_color):
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return r, g, b

def parse_color_argument(color):
    # Hex: Just one input argument
    rgb = color[0]
    r, g, b = hex_to_decimal(rgb)

    # RGB: Three base10 input arguments
    # TODO

    return r, g, b

def get_x_color():
    # Get current primary color used by pywal, which is color1 in Xresources
    # Colors could also be read from ~/.cache/wal/colors.json, but this way it
    # doesn't depend on pywal, in case the X colors are set from a different origin
    output = subprocess.check_output(
            "xrdb -query | grep \"*color1:\" | awk -F '#' '{print $2}'", 
            shell=True)
    rgb = output.decode()
    r, g, b = hex_to_decimal(rgb)

    return r, g, b

def main(args):
    """ Main entry point of the app """

    # -------------------------------------------------------------------------
    # COLORS

    r = 0
    g = 0
    b = 0

    if(args.color):
        # Set colors from input argument
        r, g, b = parse_color_argument(args.color)

    else:
        # Use X colors as fallback if no color argument is set
        # TODO: Maybe also add argument to pull colors from
        # ~/.cache/wal.colors.jason
        r, g, b = get_x_color()

    if args.verbose:
        print("RBG: ")
        sys.stdout.write(str(r) + " ")
        sys.stdout.write(str(g) + " ")
        sys.stdout.write(str(b) + "\n\n")

    # -------------------------------------------------------------------------
    # DEVICES
    # Create a DeviceManager. This is used to get specific devices
    device_manager = DeviceManager()

    if args.verbose:
        print("Found {} Razer devices".format(len(device_manager.devices)))

    # Disable daemon effect syncing.
    # Without this, the daemon will try to set the lighting effect to every device.
    device_manager.sync_effects = False

    # Iterate over each device and set the effect
    for device in device_manager.devices:
        if args.verbose:
            print("Setting device: {} to effect {}".format(device.name, args.effect))
            if not device.fx.has(args.effect):
                print("Device does not support chosen effect. Using static"
                        " as fallback...")
                args.effect = "static"

        if (args.effect == "static"):
            # Set the effect to static, requires colors in 0-255 range
            device.fx.static(r, g, b)

        elif (args.effect == "breath"):
            # TODO: Maybe add 'breath_dual' with primary and secondary color
            device.fx.breath_single(r, g, b)

        elif (args.effect == "reactive"):
            times = [razer_constants.REACTIVE_500MS, razer_constants.REACTIVE_1000MS,
            razer_constants.REACTIVE_1500MS, razer_constants.REACTIVE_2000MS]
            # TODO: Add choice for time maybe
            device.fx.reactive(r, g, b, times[3])

        elif (args.effect == "ripple"):
            device.fx.ripple(r, g, b, razer_constants.RIPPLE_REFRESH_RATE)


if __name__ == "__main__":
    """ This is executed when run from the command line """

    # -------------------------------------------------------------------------
    # ARGS
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--effect",
                        help="set effect (default: %(default)s)",
                        choices=["static","breath","reactive", "ripple"],
                        default="static",
                        action="store")

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument('-c','--color', nargs='+',
                        help="choose color (default: X color1), use one argument "
                             "for hex, or three for base10 rgb")

    args = parser.parse_args()

    if args.verbose:
        print("Starting Razer colors script...")

    main(args)
