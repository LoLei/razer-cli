# https://github.com/openrazer/openrazer/blob/feature_docs/examples/basic_effect.py

import subprocess, sys
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants

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

print("Found color1 RGB: {}".format(rgb))

print("In decimal: ")
r = int(rgb[0:2], 16)
sys.stdout.write(str(r) + " ")
g = int(rgb[2:4], 16)
sys.stdout.write(str(g) + " ")
b = int(rgb[4:6], 16)
sys.stdout.write(str(b) + "\n\n")

# -----------------------------------------------------------------------------
# DEVICES
# Create a DeviceManager. This is used to get specific devices
device_manager = DeviceManager()

print("Found {} Razer devices".format(len(device_manager.devices)))

# Disable daemon effect syncing.
# Without this, the daemon will try to set the lighting effect to every device.
device_manager.sync_effects = False

# Iterate over each device and set the effect
for device in device_manager.devices:
    print("Setting {} to static".format(device.name))

    # Set the effect, requires colors in 0-255 range
    device.fx.static(r, g, b)
