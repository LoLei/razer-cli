#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lorenz Leitner"
__version__ = "1.5.2"
__license__ = "GPL-3.0"

# Libraries
import subprocess
import sys
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import argparse

# Own
from razer_cli import util
from razer_cli import settings

# Global
args = 0


def parse_color_argument(color):
    r = 0
    g = 0
    b = 0

    if len(color) == 1:
        # Hex: Just one input argument
        rgb = color[0]
        r, g, b = util.hex_to_decimal(rgb)
    elif len(color) == 3:
        # RGB: Three base10 input arguments
        r = int(color[0])
        g = int(color[1])
        b = int(color[2])

    return r, g, b


def get_x_color():
    # Get current primary color used by pywal, which is color1 in Xresources
    # Colors could also be read from ~/.cache/wal/colors.json, but this way it
    # doesn't depend on pywal, in case the X colors are set from a different origin
    output = subprocess.check_output(
        "xrdb -query | grep \"*color1:\" | awk -F '#' '{print $2}'",
        shell=True).strip()

    if not output:
        return 0, 0, 0

    rgb = output.decode()
    r, g, b = util.hex_to_decimal(rgb)

    return r, g, b


def set_color(color):
    """ Set the color either from the input argument or use a fallback color """

    r = 0
    g = 0
    b = 0

    if(color):
        # Set colors from input argument
        r, g, b = parse_color_argument(color)

    else:
        # Use X colors as fallback if no color argument is set
        # TODO: Maybe also add argument to pull colors from
        # ~/.cache/wal.colors.jason
        r, g, b = get_x_color()

    if args.verbose:
        print("RBG:", "\n",
              '    ', r, g, b)

    return [r, g, b]


def get_effects_of_device(device):
    return [effect for effect in settings.EFFECTS if device.fx.has(effect)]


def list_devices(device_manager):
    """
    List all connected Razer devices
    https://github.com/openrazer/openrazer/blob/master/examples/list_devices.py
    """

    print("Found {} Razer devices".format(len(device_manager.devices)))

    # Iterate over each device and pretty out some standard information about each
    for device in device_manager.devices:
        if device.has('name'):
            print("{}:".format(device.name))
        else:
            print("unknown device:")
        if device.has('type'):
            print("   type: {}".format(device.type))
        if device.has('dpi'):
            print("   DPI: {}".format(device.dpi))
            print("   max DPI: {}".format(device.max_dpi))
            if(device.has('available_dpi')):
                print("   available DPI: {}".format(device.available_dpi))
        if device.has('poll_rate'):
            print("   polling rate: {}".format(device.poll_rate))
        if device.has('battery'):
            print("   battery: {}".format(device.battery))
        if device.has('brightness'):
            print("   brightness: {}".format(device.brightness))
        if device.has('lighting_logo_brightness'):
            print("   brightness (logo): {}".format(
                device.fx.misc.logo.brightness))
        if device.has('lighting_scroll_brightness'):
            print("   brightness (wheel): {}".format(
                device.fx.misc.scroll_wheel.brightness))
        if device.has('lighting_left_brightness'):
            print("   brightness (left): {}".format(
                device.fx.misc.left.brightness))
        if device.has('lighting_right_brightness'):
            print("   brightness (right): {}".format(
                device.fx.misc.right.brightness))
        if device.has('serial'):
            print("   serial: {}".format(device.serial))
        if device.has('firmware_version'):
            print("   firmware version: {}".format(device.firmware_version))
        print("   driver version: {}".format(device.driver_version))

        device_effects = get_effects_of_device(device)
        print("   effects: {}".format(device_effects))

        if (args.list_devices_long):
            print("   capabilities: {}".format(device.capabilities))
        elif (args.list_devices_long_human):
            print("   capabilities:")
            for i in device.capabilities:
                print("      ", i, "=", device.capabilities[i])
    print()


def set_dpi(device_manager):
    # Iterate over each device and set DPI
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and device.name in args.device) or (not args.device):
            if (device.type != "mouse"):
                if args.verbose:
                    print("Device {} is not a mouse".format(device.name))
            elif args.dpi == "print":
                dpi = str(device.dpi)[1:-1].split(', ')
                if args.poll == "print":
                    if dpi[0] == dpi[1]:
                        print('dpi:', dpi[0])
                    else:
                        print('dpi:', dpi[0], dpi[1])
                else:
                    if dpi[0] == dpi[1]:
                        print(dpi[0])
                    else:
                        print(dpi[0], dpi[1])
            else:
                if args.verbose:
                    print("Setting DPI of device {} to {}".format(device.name,
                                                                  args.dpi))

                # Save used settings for this device to a file
                util.write_settings_to_file(device, dpi=args.dpi)

                # Actually set DPI
                args.dpi = args.dpi.split(',')
                if len(args.dpi) == 1:
                    args.dpi.append(int(args.dpi[0]))
                device.dpi = (int(args.dpi[0]), int(args.dpi[1]))


def set_poll_rate(device_manager):
    # Iterate over each device and set Polling Rate
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and device.name in args.device) or (not args.device):
            if device.has("poll_rate"):
                if args.poll == "print":
                    if args.dpi == "print":
                        print('poll_rate:', device.poll_rate)
                    else:
                        print(device.poll_rate)
                else:
                    if args.verbose:
                        print(
                            "Setting polling rate of device {} to {}".format(
                                device.name,
                                args.poll))

                    # Actually set Polling Rate
                    device.poll_rate = int(args.poll)
            else:
                print("Device does not support setting the polling rate")


def set_brightness(device_manager):
    # Iterate over each device and set DPI
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and device.name in args.device) or (not args.device):
            if args.verbose:
                print("Setting brightness of device {}:".format(device.name))

            brightness = args.brightness

            if 'all' in brightness.keys():
                brightness['generic'] = brightness['all']
                brightness['logo'] = brightness['all']
                brightness['scroll'] = brightness['all']
                brightness['left'] = brightness['all']
                brightness['right'] = brightness['all']
                del brightness['all']
            if 'wheel' in brightness.keys() and not device.has('lighting_wheel_brightness'):
                brightness['scroll'] = brightness['wheel']
                del brightness['wheel']
                if args.verbose:
                   print('    Device does not support "wheel" assuming "scroll"')
            if args.verbose:
                print('    Input data:', brightness)
            for i in brightness:
                if i == 'generic':
                    if device.has('brightness'):
                        if args.verbose:
                            print('        Setting brightness to:',
                                  brightness[i])
                        device.brightness = int(brightness['generic'])
                        # Save used settings for this device to a file
                        util.write_settings_to_file(
                            device, brightness=brightness['generic'])
                    elif args.verbose:
                        print('        Device does not support brightness')
                elif device.has('lighting_'+i+'_brightness'):
                    if args.verbose:
                        print('        Setting lighting_'+i +
                              '_brightness to', brightness[i])
                    val = int(brightness[i])
                    if i == 'scroll':
                        i = 'scroll_wheel'
                    getattr(device.fx.misc, i).brightness = val
                elif args.verbose:
                    print('        Device does not support lighting_' +
                          i+'_brightness')


def reset_device_effect(device):
    # Set the effect to static, requires colors in 0-255 range
    try:
        # Avoid checking for device type
        # Keyboard - doesn't throw
        device.fx.static(0, 0, 0)
        # Mouse - throws
        device.fx.misc.logo.static(0, 0, 0)
        device.fx.misc.scroll_wheel.static(0, 0, 0)
        device.fx.misc.left.static(0, 0, 0)
        device.fx.misc.right.static(0, 0, 0)
    except:
        pass


def set_effect_to_device(device, effect, color, effect_args=[]):
    # Reset device effect to blank
    reset_device_effect(device)

    # Save used settings for this device to a file
    util.write_settings_to_file(device, effect, color)

    r = color[0]
    g = color[1]
    b = color[2]

    if (effect == "static"):
        # Set the effect to static, requires colors in 0-255 range
        try:
            # Avoid checking for device type
            # Keyboard - doesn't throw
            device.fx.static(r, g, b)
            # Mouse - throws
            device.fx.misc.logo.static(r, g, b)
            device.fx.misc.scroll_wheel.static(r, g, b)
            device.fx.misc.left.static(r, g, b)
            device.fx.misc.right.static(r, g, b)
        except:
            pass

    elif (effect == "breath_single"):
        device.fx.breath_single(r, g, b)

    elif (effect == "reactive"):
        times = [razer_constants.REACTIVE_500MS, razer_constants.REACTIVE_1000MS,
                 razer_constants.REACTIVE_1500MS, razer_constants.REACTIVE_2000MS]
        device.fx.reactive(r, g, b, times[3])

    elif (effect == "ripple"):
        device.fx.ripple(r, g, b, razer_constants.RIPPLE_REFRESH_RATE)

    elif (effect == "starlight_random"):
        device.fx.starlight_random(razer_constants.STARLIGHT_NORMAL)

    elif (effect == "starlight_single"):
        device.fx.starlight_single(r, g, b, razer_constants.STARLIGHT_NORMAL)

    elif (effect == "multicolor"):
        cols = device.fx.advanced.cols
        rows = device.fx.advanced.rows

        # Use supplied colors and distribute them evenly if colors are supplied
        colors_to_dist = []
        if effect_args:
            colors_to_dist = [util.hex_to_decimal(c) for c in effect_args]
        # Use random colors if no colors are supplied
        else:
            colors_to_dist = [util.get_random_color_rgb() for _ in
                              range(cols*rows)]

        try:
            counter = 0
            for row in range(rows):
                for col in range(cols):
                    device.fx.advanced.matrix.set(row, col,
                                                  colors_to_dist[counter % len(colors_to_dist)])
                    counter += 1
            # device.fx.advanced.draw_fb_or()
            device.fx.advanced.draw()
        except (AssertionError, ValueError) as e:
            if args.verbose:
                print("Warning: " + str(e))

    else:
        print("Effect is supported by device but not yet implemented.\n"
              "Consider opening a PR:\n"
              "https://github.com/LoLei/razer-x-color/pulls")
        return

    print("Setting device: {} to effect {}".format(device.name,
                                                   effect))


def set_effect_to_all_devices(device_manager, input_effect, color,
                              effect_args=[]):
    """ Set one effect to all connected devices, if they support that effect """

    # Iterate over each device and set the effect
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and device.name in args.device) or (not args.device):
            if not input_effect:
                effect_to_use = "static"
            else:
                effect_to_use = input_effect

            if ((not device.fx.has(effect_to_use)) and (effect_to_use not in
                                                        settings.CUSTOM_EFFECTS)):
                effect_to_use = "static"
                if args.verbose:
                    print("Device does not support chosen effect (yet). Using "
                          " static as fallback...")

            set_effect_to_device(device, effect_to_use, color, effect_args)


def read_args():
    # -------------------------------------------------------------------------
    # ARGS
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--effect",
                        help="set effect",
                        action="store",
                        nargs="+")

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-c", "--color", nargs="+",
                        help="choose color (default: X color1), use one argument "
                             "for hex, or three for base10 rgb")

    parser.add_argument("-l", "--list_devices",
                        help="list available devices and their supported effects",
                        action="store_true")

    parser.add_argument("-ll", "--list_devices_long",
                        help="list available devices and all their capabilities",
                        action="store_true")

    parser.add_argument("-llh", "--list_devices_long_human",
                        help="list devices and capabilities human readable",
                        action="store_true")

    parser.add_argument("-a", "--automatic",
                        help="try to find colors and set them to all devices "
                             "without user arguments, uses X or pywal colors",
                        action="store_true")

    parser.add_argument("-d", "--device", nargs="+",
                        help="only affect these devices, same name as output "
                             "of -l")

    parser.add_argument("--dpi", help="set DPI of device"
                        " (use print as a value to show it)",
                        action="store")

    parser.add_argument("--poll",
                        help="set polling rate of device"
                        " (use print as a value to show it)",
                        action="store")

    parser.add_argument("-b", "--brightness", nargs="+",
                        help="set brightness of device",
                        dest='brightness',
                        action="store")

    parser.add_argument("--sync",
                        help="sync lighting effects to all supported "
                        "Razer products",
                        action="store_true")

    global args
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)


def main():
    """ Main entry point of the app """

    read_args()

    # -------------------------------------------------------------------------
    # DEVICES
    # Create a DeviceManager. This is used to get specific devices
    device_manager = DeviceManager()

    # Disable daemon effect syncing.
    # Without this, the daemon will try to set the lighting effect to every
    # device.
    device_manager.sync_effects = args.sync

    # Do below only if dry run is not specified
    if args.automatic or args.effect or args.color:
        # ----------------------------------------------------------------------
        # COLORS
        color = set_color(args.color)

        if args.effect:
            set_effect_to_all_devices(device_manager, args.effect[0], color,
                                      args.effect[1:])
        else:
            set_effect_to_all_devices(device_manager, args.effect, color)

    if args.dpi:
        set_dpi(device_manager)

    if args.poll:
        set_poll_rate(device_manager)

    if args.brightness:
        i = len(args.brightness)
        if i == 1 and args.brightness[0].isnumeric():
            args.brightness = {"all": args.brightness[0]}
            set_brightness(device_manager)
        elif i % 2 == 0:
            brightness = {}
            i = i-1
            while i > -1:
                name = args.brightness[i-1]
                value = args.brightness[i]
                if args.brightness[i].isnumeric():
                    brightness[name] = value
                #elif args.verbose:
                else:
                    print('Warning:', value, 'is not a number for',
                          name, '[Skipping]')
                i = i-2
            args.brightness = brightness
            set_brightness(device_manager)
        else:
            print('Invalid brightness input, example:\n',
                  '    -b 50\n',
                  '    -b all 50\n',
                  '    -b generic 50 logo 25\n',
                  '    -b scroll 50 logo 25\n',
                  '    -b left 25 right 75 logo 0 scroll 50')

    if (args.list_devices or args.list_devices_long or
            args.list_devices_long_human):
        list_devices(device_manager)


if __name__ == "__main__":
    """ This is executed when run from the command line - obsolete """

    main()
