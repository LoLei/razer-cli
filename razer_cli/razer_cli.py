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

    if len(color) == 1:
        # Hex: Just one input argument
        rgb = color[0]
        if rgb.lower() == "random":
            rgb = util.get_random_color_rgb()
        else:
            rgb = util.hex_to_decimal(rgb)
    else:
        if len(color) == 3:
            # RGB: Three base10 input arguments
            rgb = []
            for i in color:
                if lower(color) == "rng":
                    rgb.append(util.randint(0, 255))
                else:
                    rgb.append(int(color[i]))
        else:
            print("Unknown color input:", color)
            rgb = get_random_color_rgb()

    return rgb


def parse_zones(zones_list):
    everything = settings.ZONES
    if not zones_list:
        # Known zone names, generic is a fake name for internal use
        return [everything]
    zones = []
    stop = len(zones_list)
    i = 0
    while i < stop:
        if zones_list[i] == 'all':
            zones.append(everything)
        else:
            zones.append(zones_list[i].split(','))
        i += 1
    return zones


def get_x_color():
    # Get current primary color used by pywal, which is color1 in Xresources
    # Colors could also be read from ~/.cache/wal/colors.json, but this way it
    # doesn't depend on pywal, in case the X colors are set from a different origin
    output = subprocess.check_output(
        "xrdb -query | grep \"*color1:\" | awk -F '#' '{print $2}'",
        shell=True).strip()

    if not output:
        #return [0, 0, 0]
        return util.get_random_color_rgb()

    return util.hex_to_decimal(output.decode())


def get_rgb(c):
    # Input array; output variables
    return c[0], c[1], c[2]


def set_color(color):
    """ Set the color either from the input argument or use a fallback color """

    RGB = []

    if(color):
        # Set colors from input argument
        stop = len(color)
        i = 0
        while i < stop:
            if len(color[i]) > 3:
                if not len(color[i]) == 6:
                    print('color', len(RGB)+1,
                          '(', color[i], ') looks to have a typo')
                RGB.append(parse_color_argument([color[i]]))
                i += 1
            elif stop > i+2:
                if len(color[i]) > 3 or len(color[i+1]) > 3 or len(color[i+2]) > 3:
                    print('color', len(
                        RGB)+1, '(', color[i], color[i+1], color[i+2], ') looks to have a typo')
                rgb = [color[i], color[i+1], color[i+2]]
                RGB.append(parse_color_argument(rgb))
                i += 3
            else:
                print("Unexpected arguments for color")
                break
        #r, g, b = parse_color_argument(color)

    else:
        # Use X colors as fallback if no color argument is set
        # TODO: Maybe also add argument to pull colors from
        # ~/.cache/wal.colors.jason
        RGB.append(get_x_color())

    if args.verbose:
        print("RGB:")
        i = 0
        stop = len(RGB)
        while i < stop:
            print('   ', RGB[i])
            i += 1
        print('    If more are needed random ones will be generated')

    return RGB


def get_effects_of_device(device):
    zones = {}
    delete = []
    for i in settings.ZONES:
        if i == 'generic':
            prop = device.fx
        else:
            prop = getattr(device.fx.misc, i)
        zones[i] = [
            effect for effect in settings.EFFECTS if hasattr(prop, effect)]
        if(hasattr(prop, 'advanced')):
            for e in settings.CUSTOM_EFFECTS:
                zones[i].append(e)
        if len(zones[i]) == 0:
            delete.append(i)
    for i in delete:
        zones.pop(i)
    return zones


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

        capabilitity = {"supported": [], "unsupported": []}
        device_effects = get_effects_of_device(device)
        for i in device.capabilities:
            if device.capabilities[i]:
                capabilitity['supported'].append(i)
            elif args.verbose:
                capabilitity['unsupported'].append(i)

        join_str = ', '
        start_str = ''
        if args.list_devices_long:
            join_str = '\n      '
            start_str = '\n     '
        print("   supported capabilities:"+start_str,
              join_str.join(capabilitity['supported']))
        if args.verbose:
            print("   unsupported capabilities:"+start_str,
                  join_str.join(capabilitity['unsupported']))
        for i in device_effects:
            print('   lighting zone', i, 'supports:' +
                  start_str, join_str.join(device_effects[i]))
        print()


def set_dpi(device_manager):
    # Iterate over each device and set DPI
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and device.name in args.device) or (not args.device):
            if (not device.has('dpi')):
                if args.verbose:
                    print("Device {} is not have a DPI setting".format(device.name))
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

                    # Save used settings for this device to a file
                    util.write_settings_to_file(device, poll=args.poll)

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
            # Save used settings for this device to a file
            util.write_settings_to_file(device, brightness=brightness)


def reset_device_effect(device):
    # Set the effect to static, requires colors in 0-255 range
    device.fx.static(0, 0, 0)
    for i in ['logo', 'scroll_wheel', 'left', 'right']:
        ele = getattr(device.fx.misc, i)
        if ele:
            ele.static(0, 0, 0)


def set_effect_to_device(device, effects, color, zones):
    # Known Effects: advanced, breath_dual, breath_random, breath_single,
    #    breath_triple, none, reactive, ripple, ripple_random, spectrum,
    #    starlight_dual, starlight_random, starlight_single, static, wave

    # Reset device effect to blank (but why? oh multicolor is why)
    # Perhaps we should check the settings file for multicolor?
    #reset_device_effect(device)

    c_used = 0
    i = 0
    stop = len(zones)
    while i < stop:
        arg = effects[i].split(',')
        effect = arg[0]
        arg.pop(0)
        used = 0
        for zone in zones[i]:
            if zone == 'generic':
                prop = device.fx
            else:
                prop = False
                if not hasattr(device.fx.misc, zone) and zone in ["scroll", "wheel"]:
                    if args.verbose:
                        print('   ', zone, 'is not valid, assuming scroll_wheel')
                    zone = "scroll_wheel"
                if hasattr(device.fx.misc, zone):
                    prop = getattr(device.fx.misc, zone)
            if prop:
                support = False
                if hasattr(prop, effect) or effect in ["multicolor"]:
                    if effect in ['none', 'breath_random', 'spectrum']:
                        used = 0
                        if getattr(prop, effect)() and args.verbose:
                            print("    Setting", zone, "to", effect)
                            support = True
                    elif effect in ['static', 'breath_single']:
                        used = 1
                        if len(color) < c_used+used:
                            color.append(util.get_random_color_rgb())
                        r, g, b = get_rgb(color[c_used])
                        if getattr(prop, effect)(r, g, b) and args.verbose:
                            print("    Setting", zone, effect, "to:", r, g, b)
                            support = True
                    elif effect == 'breath_dual':
                        used = 2
                        while len(color) < c_used+used:
                            color.append(util.get_random_color_rgb())
                        r, g, b = get_rgb(color[c_used])
                        r2, g2, b2 = get_rgb(color[c_used+1])
                        if getattr(prop, effect)(r, g, b, r2, g2, b2) and args.verbose:
                            print("    Setting", zone, effect,
                                  "to:\n        [", r, g, b, ']\n        [', r2, g2, b2, ']')
                            support = True
                    elif effect == 'breath_triple':
                        used = 3
                        while len(color) < c_used+used:
                           color.append(util.get_random_color_rgb())
                        r, g, b = get_rgb(color[c_used])
                        r2, g2, b2 = get_rgb(color[c_used+1])
                        r3, g3, b3 = get_rgb(color[c_used+2])
                        if getattr(prop, effect)(r, g, b, r2, g2, b2, r3, g3, b3) and args.verbose:
                            print("    Setting", zone, effect,
                                  "to:\n        [", r, g, b, ']\n        [', r2, g2, b2, ']\n        [', r3, g3, b3, ']')
                            support = True
                    elif effect == 'reactive':
                        used = 1
                        if len(color) < c_used+used:
                            color.append(util.get_random_color_rgb())
                        # These are just numbers 1-4
                        #time = [razer_constants.REACTIVE_500MS, razer_constants.REACTIVE_1000MS, razer_constants.REACTIVE_1500MS, razer_constants.REACTIVE_2000MS]
                        if len(arg) == 0:
                            time = util.randint(1, 4)
                        else:
                            time = int(arg[0])
                        if getattr(prop, effect)(*color[c_used], time) and args.verbose:
                            print("    Setting", zone, effect, "to:", *
                                  color[c_used], '@ timing level', time)
                            support = True
                    elif effect == 'ripple':
                        used = 1
                        if len(color) < c_used+used:
                            color.append(util.get_random_color_rgb())
                        r, g, b = get_rgb(color[c_used])
                        if getattr(prop, effect)(r, g, b, razer_constants.RIPPLE_REFRESH_RATE) and args.verbose:
                            print("    Setting", zone, effect, "to:", r, g, b)
                            support = True
                    elif effect == 'ripple_random':
                        used = 0
                        if getattr(prop, effect)(razer_constants.RIPPLE_REFRESH_RATE) and args.verbose:
                            print("    Setting", zone, "to", effect)
                            support = True
                    elif effect == 'starlight_single':
                        used = 1
                        if len(color) < c_used+used:
                            color.append(util.get_random_color_rgb())
                        # These are just numbers 1-3
                        #time = [razer_constants.STARLIGHT_FAST, razer_constants.STARLIGHT_NORMAL, razer_constants.STARLIGHT_SLOW]
                        if len(arg) == 0:
                            time = util.randint(1, 3)
                        else:
                            time = int(arg[0])
                        if getattr(prop, effect)(*color[c_used], time) and args.verbose:
                            print("    Setting", zone, effect, "to:", *
                                  color[c_used], '@ timing level', time)
                            support = True
                    elif effect == 'starlight_dual':
                        used = 2
                        if len(color) < c_used+used:
                            color.append(util.get_random_color_rgb())
                        # These are just numbers 1-3
                        #time = [razer_constants.STARLIGHT_FAST, razer_constants.STARLIGHT_NORMAL, razer_constants.STARLIGHT_SLOW]
                        if len(arg) == 0:
                            time = util.randint(1, 3)
                        else:
                            time = int(arg[0])
                        if getattr(prop, effect)(*color[c_used], *color[c_used+1], time) and args.verbose:
                            print("    Setting", zone, effect, " @ timing level", time,
                                  "to:\n        [", *color[c_used], ']\n        [', *color[c_used+1])
                            support = True
                    elif effect == 'starlight_random':
                        used = 0
                        if len(arg) == 0:
                            time = util.randint(1, 3)
                        else:
                            time = int(arg[0])
                        if getattr(prop, effect)(time) and args.verbose:
                            print("    Setting", zone, "to",
                                  effect, '@ timing level', time)
                            support = True
                    elif effect == 'wave':
                        used = 0
                        # These are just numbers 1-2
                        #direction=[razer_constants.WAVE_LEFT, razer_constants.WAVE_RIGHT]
                        if len(arg) == 0:
                            direction = util.randint(1, 2)
                        else:
                            direction = int(arg[0])
                        if getattr(prop, effect)(direction) and args.verbose:
                            print("    Setting", zone, "to",
                                  effect, ' in direction', direction)
                            support = True
                    elif effect == 'brightness':
                        used = 0
                        if len(arg) == 0:
                            b = 100
                        else:
                            b = int(arg[0])
                        prop.brightness = b
                        if args.verbose:
                            print("    Setting", zone, effect, 'to', b)
                            support = True
                    elif effect == 'multicolor':
                        if hasattr(prop, 'advanced'):
                            if len(arg) > 0:
                                used = int(arg[0])
                            else:
                                used = 0
                            while len(color) < c_used+used:
                                color.append(util.get_random_color_rgb())
                            cols = prop.advanced.cols
                            rows = prop.advanced.rows
                            if used == 0:
                                colors_to_dist = [
                                    util.get_random_color_rgb() for _ in range(cols*rows)]
                            else:
                                colors_to_dist = []
                                end = len(color)
                                start = c_used
                                while start < end:
                                    colors_to_dist.append(color[start])
                                    start += 1
                            try:
                                counter = 0
                                for row in range(rows):
                                    for col in range(cols):
                                        device.fx.advanced.matrix.set(
                                            row, col, colors_to_dist[counter % len(colors_to_dist)])
                                        counter += 1
                                # device.fx.advanced.draw_fb_or()
                                device.fx.advanced.draw()
                                if args.verbose:
                                    print("    Setting", zone, "to",
                                          effect, "\n        ", colors_to_dist)
                                support = True
                            except (AssertionError, ValueError) as e:
                                if args.verbose:
                                    print("    Warning: " + str(e))
                    else:
                        print("    Sorry", effect, "is supported by the hardware, but this software does not\n",
                              "       Consider makeing a bug report:\n",
                              "           https://github.com/LoLei/razer-cli/issues")
                if args.verbose and not support:
                    print("   ", zone, "does not support", effect)
            elif args.verbose:
                print("    Device does not support", zone)
        c_used += used
        i += 1
    # Save used settings for this device to a file
    util.write_settings_to_file(device, effects, color, zones=zones)


def set_effect_to_all_devices(device_manager, input_effects, color, zones):
    """ Set one effect to all connected devices, if they support that effect """

    # Iterate over each device and set the effect
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and device.name in args.device) or (not args.device):
            if args.verbose:
                print('Setting effects for {}:'.format(device.name))
            set_effect_to_device(device, input_effects, color, zones)


def read_args():
    # -------------------------------------------------------------------------
    # ARGS
    parser = argparse.ArgumentParser()

    parser.add_argument("-man", "--manual", nargs="*",
                        help="Print help details for given feature(s)",
                        action="store")

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-d", "--device", nargs="+",
                        help="only affect these devices, same name as output "
                             "of -l")

    parser.add_argument("-a", "--automatic",
                        help="try to find colors and set them to all devices "
                             "without user arguments, uses X or pywal colors",
                        action="store_true")

    parser.add_argument("-e", "--effect",
                        help="set effect",
                        action="store",
                        nargs="+")

    parser.add_argument("-c", "--color", nargs="+",
                        help="choose color (default: X color1), use one argument "
                             "for hex, or three for base10 rgb")

    parser.add_argument("-z", "--zone", nargs="+",
                        dest='zones',
                        help="choose zone for color(s)")

    parser.add_argument("-b", "--brightness", nargs="+",
                        help="set brightness of device",
                        dest='brightness',
                        action="store")

    parser.add_argument("--dpi", help="set DPI of device"
                        " (use print as a value to show it)",
                        action="store")

    parser.add_argument("--poll",
                        help="set polling rate of device"
                        " (use print as a value to show it)",
                        action="store")

    parser.add_argument("-l", "--list_devices",
                        help="list available devices and their supported capabilities/effects",
                        action="store_true")

    parser.add_argument("-ll", "--list_devices_long",
                        help="list available devices and list their supported capabilities/effects",
                        action="store_true")

    parser.add_argument("--sync",
                        help="sync lighting effects to all supported "
                        "Razer products",
                        action="store_true")

    parser.add_argument("--restore",
                        help="Load last used settings",
                        action="store_true")
    global args
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)


def main():
    """ Main entry point of the app """

    read_args()
    if not args.manual == None:
        match = False
        if 'color' in args.manual:
            match = True
            print("Color arguments can be and of the following:\n",
                  "   Hex Codes (FF00FF)\n",
                  "   RGB (255 0 255)\n",
                  "   RNG (RANDOM)\n",
                  "   You can mix these as you please EG:\n",
                  "       --color RANDOM 255 0 255 FF00FF\n",
                  "   If a lack of colors are provided random ones will be generated\n")
        if 'brightness' in args.manual:
            match = True
            print("Brightness arguments can be and of the following:\n",
                  "   The following words are valid:\n",
                  "       "+(', '.join(settings.ZONES))+", and all\n",
                  "   -b 50 (set everything to 50)\n",
                  "   -b all 50 (set everything to 50)\n",
                  "   -b generic 50 logo 25 (set generic to 50 and logo to 25)\n",
                  "   -b scroll 50 logo 25 (set scroll to 50 and logo to 25)\n",
                  "   -b left 25 right 75 logo 0 scroll 50 (set left to 25, right to 75, and scroll to 25)\n")
        if 'zone' in args.manual:
            match = True
            print("Zone arguments can be name your device supports",
                  "\nKnown zone names are " +
                  (', '.join(settings.ZONES))+", and all.",
                  "\nEach zone group gets it own color(s)"
                  "\nFor example if your zone is '-z logo,scroll_wheel' this will use the same color(s) for both zones",
                  "\nhowever if you use '-z logo scroll_wheel' this will different color(s) for each zones.",
                  "\nYou can mix these are you see fit for example: '-z logo,scroll_wheel left right'",
                  "\nEach zone argument gets it own effect, the default zone is '" +
                  (','.join(settings.ZONES))+"'",
                  "\nAll is treated as '"+(','.join(settings.ZONES))+"'\n")
        if 'effect' in args.manual:
            match = True
            print("Effect arguments can any of the following:\n",
                  "   breath_dual, breath_random, breath_single, breath_triple, none, reactive, ripple, ripple_random, spectrum, starlight_dual, starlight_random, starlight_single, static, wave, and multicolor",
                  "\nEach effect is applied to 1 zone, remember that 'logo,right' is 1 zone and 'left right' is 2 zones"
                  "\nThe following effects support a second argument by adding a comma followed by a number:\n",
                  "   brightness, reactive, starlight_single, starlight_dual, starlight_random, wave, and multicolor\n",
                  "   brightness,[0-100]\n",
                  "       % brightness (this is the PWM Duty Cycle)\n",
                  "       If not specified it will be 100\n",
                  "       This is the same things as --brightness\n",
                  "       Example usage:\n",
                  "           razer-cli -e static brightness,75 -z logo logo -c FF0000",
                  "   reactive,[1-4]\n",
                  "       1 = 500ms, 2 = 1000ms, 3 = 1500ms, and 4 = 2000ms\n",
                  "       If not specified it will be chosen at random\n",
                  "   starlight_single,[1-3], starlight_dual,[1-3], and starlight_random,[1-3]\n",
                  "       1 = fast, 2 = normal, and 3 = slow\n",
                  "       If not specified it will be chosen at random\n",
                  "   wave,[1-2]\n",
                  "       1 = right and 2 = left\n",
                  "       If not specified it will be chosen at random\n",
                  "   multicolor,[0-∞]\n",
                  "       0 = assign random colors for everything (does not consume colors)\n",
                  "       1-∞ = the number of colors to use from -c\n",
                  "       This defaults to 0\n",
                  "   The following effects do NOT consume colors:\n",
                  "       none, brightness, breath_random, spectrum, starlight_random, and wave\n")
        if 'poll' in args.manual:
            match = True
            print("Poll lets you assign the polling rate of a device (like a mouse)",
                  "\nThis can be set to 125, 500, or 1000; 500 is default",
                  "\nYou can also use 'print' to see the poll rate\n")
        if 'dpi' in args.manual:
            match = True
            print("DPI lets you assign the dpi a device (like a mouse)",
                  "\nThis needs to be a number or 2 numbers separated by a command (800,1000)",
                  "\nWhen using 2 numbers you are setting the X/Y DPI separately in that order"
                  "\nYou can also use 'print' to see the dpi setting")
        if not match:
            print(
                "Manual entries exist for color, brightness, zone, effect, poll, and dpi")
        return

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
        zones = parse_zones(args.zones)
        if not args.effect:
            effects = ['static']
        else:
            effects = args.effect

        stop = len(zones)
        if len(effects) == 1 and stop > 1:
            while len(effects) < stop:
                effects.append(effects[0])

        set_effect_to_all_devices(device_manager, effects, color, zones)
    if args.restore:
        util.load_settings_from_file(args.verbose)

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
            # Even number of arguments
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
            print("Invalid brightness input, see `razer-cli --manual brightness'")

    if args.list_devices or args.list_devices_long:
        list_devices(device_manager)


if __name__ == "__main__":
    """ This is executed when run from the command line - obsolete """

    main()
