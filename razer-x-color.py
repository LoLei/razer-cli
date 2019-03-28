# https://github.com/openrazer/openrazer/blob/feature_docs/examples/basic_effect.py

import subprocess, sys
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import argparse

# TODO: Pivot maybe, this thing now almost functions as a CLI for Razer, just
# add the colors as an additional input argument, use Xresources colors as
# fallback

# -----------------------------------------------------------------------------
# ARGS

parser = argparse.ArgumentParser()
parser.add_argument("--effect", help="set effect (default: %(default)s)",
                    choices=["static","breath","reactive", "ripple"],
                    default="static",
                    action="store")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

if args.verbose:
    print("Starting Razer colors script...")

# -----------------------------------------------------------------------------
# COLORS
# Get current primary color used by pywal
output = subprocess.check_output(
        "xrdb -query | grep \"*color1:\" | awk -F '#' '{print $2}'", 
        shell=True)
rgb = output.decode()
# Colors could also be read from ~/.cache/wal/colors.json, but this way it
# doesn't depend on pywal, in case the X colors are set from a different origin

r = int(rgb[0:2], 16)
g = int(rgb[2:4], 16)
b = int(rgb[4:6], 16)

if args.verbose:
    print("Found color1 RGB: {}".format(rgb))
    print("In decimal: ")
    sys.stdout.write(str(r) + " ")
    sys.stdout.write(str(g) + " ")
    sys.stdout.write(str(b) + "\n\n")

# -----------------------------------------------------------------------------
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
