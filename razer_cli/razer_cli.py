#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lorenz Leitner"
__version__ = "1.5.2"
__license__ = "GPL-3.0"

# Libraries
import sys
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import argparse

# Own
from razer_cli import util
from razer_cli import settings

# Global
args = 0


def parse_zones(zones_list):
    if not zones_list:
        return [settings.ZONES]
    zones = []
    stop = len(zones_list)
    i = 0
    while i < stop:
        if zones_list[i] == 'all':
            zones.append(settings.ZONES)
        else:
            zones.append(zones_list[i].split(','))
        i += 1
    return zones


def parse_color(color):
    """ Set the color either from the input argument or use a fallback color """

    RGB = []

    if(color):
        # Set colors from input argument
        stop = len(color)
        i = 0
        while i < stop:
            if len(color[i]) > 3 or color[i] in ['x', 'X']:
                if not len(color[i]) in [1, 6]:
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
        RGB.append(util.get_x_color(args.verbose))

    return RGB


def parse_color_argument(color):

    if len(color) == 1:
        # Hex: Just one input argument or key word
        rgb = color[0].lower()
        if rgb == "random":
            rgb = util.get_random_color_rgb()
        elif rgb == "x":
            rgb = util.get_x_color(args.verbose)
        else:
            rgb = util.hex_to_decimal(rgb)
    else:
        if len(color) == 3:
            # RGB: Three base10 input arguments
            rgb = []
            for i in color:
                if i.lower() == "rng":
                    rgb.append(util.randint(0, 255))
                else:
                    rgb.append(int(i))
        else:
            print("Unknown color input:", color)
            rgb = util.get_random_color_rgb()
    return rgb


def list_devices(device_manager):
    """
    List all connected Razer devices
    https://github.com/openrazer/openrazer/blob/master/examples/list_devices.py
    """

    if args.verbose or not args.device:
        print("Found {} Razer device(s)".format(len(device_manager.devices)))
    if args.verbose and args.device:
        print("   Only showing devices matching:", args.device)

    # Iterate over each device and pretty out some standard information about each
    for device in device_manager.devices:
        # If -d argument is set, only list those devices
        if (args.device and (device.name in args.device or device.serial in args.device)) or (not args.device):
            glue_str = ', '
            start_str = ''
            if args.list_devices_long:
                glue_str = '\n         '
                start_str = '\n        '

            if device.has('name'):
                print(device.name+':')
            else:
                print("unknown device:")
            if device.has('type'):
                print("   type:", device.type)
            # https://www.youtube.com/watch?v=rnZYEuqKGCo
            #if hasattr(device,'device_image'):
            #    print("   image url:", device.device_image)
            if device.has('dpi'):
                print("   DPI:", device.dpi)
                print("   max DPI:", device.max_dpi)
            if(device.has('available_dpi')):
                print("   available DPI:", device.available_dpi)
            if(device.has('dpi_stages')):
                print("   DPI stages:", device.dpi_stages)
            if device.has('poll_rate'):
                print("   polling rate:", device.poll_rate)
            if device.has('battery'):
                print("   battery:")
                print("      charge:", device.battery_level)
                print("      charging:", device.is_charging)
                print("      low threshold:",
                      device.get_low_battery_threshold(), '%')
                print("      idle delay", device.get_idle_time(), 'seconds')

            for i in settings.ZONES:
                # Settings
                if i == 'generic':
                    print('  ', i, 'zone:')
                    if util.rgb_support(device, effect='brightness'):
                        print("      brightness:", device.brightness)
                    elif args.verbose:
                        print("      brightness: N/A")
                    try:
                        # hasattr will error anyway; no point in testing with it
                        print("      colors:",
                              util.bytes_array_to_hex_array(device.fx.colors))
                    except:
                        if args.verbose:
                            print("      colors: N/A")
                    for e in ['active', 'effect', 'speed', 'wave_dir']:
                        try:
                            # hasattr will error anyway; no point in testing with it
                            print("      {}: {}".format(
                                e, getattr(device.fx, e)))
                        except:
                            if args.verbose:
                                print("      {}: N/A".format(e))
                elif not util.rgb_support(device, i):
                    # Zones does not exist
                    if args.verbose:
                        print('  ', i, 'zone: N/A')
                    continue
                else:
                    attr = getattr(device.fx.misc, i)
                    print('  ', i, 'zone:')
                    for p in ['brightness', 'colors', 'active', 'effect', 'speed', 'wave_dir']:
                        # Aside some of these features are not in the stable branch of openrazer as of 2021-01-30
                        try:
                            val = getattr(attr, p)
                            if isinstance(val, (bytes, bytearray)):
                                val = util.bytes_array_to_hex_array(val)
                            print("      {}: {}".format(p, val))
                        except:
                            if args.verbose:
                                print("      {}: N/A".format(p))
                # Features
                effects = {"supported": [], "unsupported": []}
                for e in settings.ALL_EFFECTS:
                    if util.rgb_support(device, i, e):
                        effects['supported'].append(e)
                    elif args.verbose:
                        effects['unsupported'].append(e)
                if len(effects['supported']) > 0:
                    print('      effects available:' +
                          start_str, glue_str.join(effects['supported']))
                if args.verbose:
                    print('      effects unavailable:' +
                          start_str, glue_str.join(effects['unsupported']))

            if device.has('serial'):
                print("   serial:", device.serial)
            if device.has('firmware_version'):
                print("   firmware version:", device.firmware_version)
            print("   driver version:", device.driver_version)

            if args.list_devices_short:
                print()
                continue

            capabilitity = {"supported": [], "unsupported": []}
            if args.list_devices_long:
                glue_str = '\n      '
                start_str = '\n     '
            for i in device.capabilities:
                if device.capabilities[i]:
                    capabilitity['supported'].append(i)
                elif args.verbose:
                    capabilitity['unsupported'].append(i)

            print("   supported capabilities:"+start_str,
                  glue_str.join(capabilitity['supported']))
            if args.verbose:
                print("   unsupported capabilities:"+start_str,
                      glue_str.join(capabilitity['unsupported']))
            print()


def set_dpi(device_manager):
    # Iterate over each device and set DPI
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and (device.name in args.device or device.serial in args.device)) or (not args.device):
            if (not device.has('dpi')):
                if args.verbose:
                    print("Device {} is not have a DPI setting".format(device.name))
            elif args.dpi == "print":
                dpi = device.dpi
                if args.poll == "print":
                    if dpi[0] == dpi[1] or args.battery and len(args.battery) == 1:
                        print('DPI:', dpi[0])
                    else:
                        print('DPI:', *dpi)
                else:
                    if dpi[0] == dpi[1]:
                        print(dpi[0])
                    else:
                        print(*dpi)
            else:
                if args.verbose:
                    print("Setting DPI of device {} to {}".format(device.name,
                                                                  args.dpi))

                # Actually set DPI
                dpi = args.dpi.split(',')
                if len(dpi) == 1:
                    dpi.append(int(dpi[0]))
                device.dpi = (int(dpi[0]), int(dpi[1]))

                # Save used settings for this device to a file
                util.write_settings_to_file(device, dpi=args.dpi)


def set_poll_rate(device_manager):
    # Iterate over each device and set Polling Rate
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and (device.name in args.device or device.serial in args.device)) or (not args.device):
            if device.has("poll_rate"):
                if args.poll == "print":
                    if args.dpi == "print" or args.battery and len(args.battery) == 1:
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

                    # Save used settings for this device to a file
                    util.write_settings_to_file(device, poll=args.poll)
            else:
                print("Device does not support setting the polling rate")


def set_battery(device_manager):
    for device in device_manager.devices:
        if (args.device and (device.name in args.device or device.serial in args.device)) or (not args.device):
            if device.has("battery"):
                if len(args.battery) < 2:
                    print(device.name, 'battery:')
                    print("   charge:", device.battery_level)
                    print("   charging:", device.is_charging)
                    print("   low threshold:",
                          device.get_low_battery_threshold(), '%')
                    print("   idle delay", device.get_idle_time(), 'seconds')
                else:
                    i = 0
                    stop = len(args.battery)
                    bat = {}
                    while i < stop:
                        if args.battery[i] == "low" and stop > i+1:
                            bat['low'] = int(args.battery[i+1])
                            device.set_low_battery_threshold(bat['low'])
                            if args.verbose:
                                print(device.name, 'low battery =',
                                      device.get_low_battery_threshold(), '%')
                        elif args.battery[i] == "idle" and stop > i+1:
                            bat['idle'] = int(args.battery[i+1])
                            device.set_idle_time(bat['idle'])
                            if args.verbose:
                                print(device.name, 'idle delay =',
                                      device.get_idle_time(), 'seconds')
                        i += 1
                    # Save used settings for this device to a file
                    util.write_settings_to_file(device, battery=bat)
            else:
                print('Does', device.name, 'have a battery?')


def set_brightness(device_manager):
    # Iterate over each device and set DPI
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and (device.name in args.device or device.serial in args.device)) or (not args.device):
            if args.verbose:
                print("Setting brightness of device {}:".format(device.name))

            brightness = args.brightness

            if 'all' in brightness.keys():
                for i in settings.ZONES:
                    brightness[i] = brightness['all']
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
                elif util.rgb_support(device, i, 'brightness'):
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
    # Currently not used, disabled in set_effect_to_device
    # Set the effect to static, requires colors in 0-255 range
    device.fx.static(0, 0, 0)
    for i in settings.ZONES:
        ele = getattr(device.fx.misc, i)
        if ele:
            ele.static(0, 0, 0)


def set_effect_to_device(device, effects, color, zones):
    # Known Effects: advanced, breath_dual, breath_random, breath_single,
    #    breath_triple, blinking, none, reactive, ripple, ripple_random,
    #    pulsate, spectrum, starlight_dual, starlight_random,
    #    starlight_single, static, wave

    # Reset device effect to blank (but why? oh multicolor is why)
    # Perhaps we should check the settings file for multicolor?
    # Enabling this will prevent setting diff zones to diff effects
    # without them being in the same command
    #reset_device_effect(device)

    if args.verbose:
        debug_msg = {}
    og_color_len = len(color)
    if og_color_len == 0:
        default_color = [util.get_x_color(args.verbose)]
    c_used = 0
    i = 0
    stop = len(zones)
    if len(effects) < stop:
        stop = len(effects)
        if args.verbose:
            print("   Warning: Only", stop,
                  "effects provided for", len(zones), "zones")
    while i < stop:
        arg = effects[i].split(',')
        effect = arg[0]
        if effect not in settings.EFFECTS and effect not in settings.CUSTOM_EFFECTS:
            print("   Warning:", effect, "is not a known effect.")
        arg.pop(0)
        used = 0
        for zone in zones[i]:
            if args.verbose:
                if zone not in debug_msg:
                    debug_msg[zone] = []
            if not util.rgb_support(device, zone, effect):
                if args.verbose:
                    if util.rgb_support(device, zone):
                        debug_msg[zone].append(['Does not support', effect])
                    else:
                        debug_msg[zone].append([zone, 'is not supported'])
                continue
            if zone == 'generic':
                prop = device.fx
            else:
                if zone in ["scroll", "wheel"]:
                    if args.verbose:
                        debug_msg[zone].append(
                            ['not valid, assuming scroll_wheel'])
                    zone = "scroll_wheel"
                    zones[i].append(zone)
                    continue
                prop = getattr(device.fx.misc, zone)
            if og_color_len == 0 and not effect in settings.COLORLESS_EFFECTS and not (effect == 'multicolor' and (len(arg) == 0 or arg[0] == '0')):
                # Lets get default colors
                # We can skip this if the effect does not need colors
                # * multicolor does NOT use consume colors if set to 0 (default)
                try:
                    # hasattr will error anyway if does not work, no point testing it
                    color = parse_color(
                        util.bytes_array_to_hex_array(getattr(prop, 'colors')))
                except:
                    color = default_color
                c_used = 0
                if args.verbose:
                    debug_msg[zone].append(["No color given, using:", color])
            if not effect in settings.ALL_EFFECTS:
                debug_msg[zone].append(["Sorry", effect, "is supported by the hardware, but this software does not\n",
                                        "         Consider makeing a bug report:\n",
                                        "            https://github.com/LoLei/razer-cli/issues"])
                continue
            # Prep colors
            used = 0
            if not effect in settings.COLORLESS_EFFECTS:
                # Custom effects do this in there own block
                used = 1
                if effect == 'breath_triple':
                    used = 3
                elif effect in ['breath_dual', 'starlight_dual']:
                    used = 2
                while len(color) < c_used+used:
                    color.append(util.get_random_color_rgb())
                # Do I really need this message?
                #if args.verbose:
                #    debug_msg[zone].append(["Using color(s):",
                #                           [*color[c_used:c_used+used]],
                #                           "\n         from:",color])
            # Set Effect
            if effect in ['none', 'breath_random', 'spectrum']:
                # Effects that use no parameters
                if getattr(prop, effect)() and args.verbose:
                    debug_msg[zone].append(["Setting to", effect])
            elif effect in ['static', 'breath_single', 'blinking', 'pulsate']:
                # Effects that use 1 color
                rgb = color[c_used]
                if getattr(prop, effect)(*rgb) and args.verbose:
                    debug_msg[zone].append(["Setting", effect, "to:", *rgb])
            elif effect == 'breath_dual':
                # Effects that use 2 colors
                rgb = color[c_used]
                rgb2 = color[c_used+1]
                if getattr(prop, effect)(*rgb, *rgb2) and args.verbose:
                    debug_msg[zone].append(["Setting", effect,
                                            "to:\n         [", *rgb, ']\n         [', *rgb2, ']'])
            elif effect == 'breath_triple':
                # Effects that use 3 colors
                rgb = color[c_used]
                rgb2 = color[c_used+1]
                rgb3 = color[c_used+2]
                if getattr(prop, effect)(*rgb, *rgb2, *rgb3) and args.verbose:
                    debug_msg[zone].append(["Setting", effect,
                                            "to:\n         [", *rgb, ']\n         [', *rgb2, ']\n         [', *rgb3, ']'])
            elif effect == 'reactive':
                # These are just numbers 1-4
                #time = [razer_constants.REACTIVE_500MS, razer_constants.REACTIVE_1000MS, razer_constants.REACTIVE_1500MS, razer_constants.REACTIVE_2000MS]
                if len(arg) == 0:
                    time = util.randint(1, 4)
                else:
                    time = int(arg[0])
                if getattr(prop, effect)(*color[c_used], time) and args.verbose:
                    debug_msg[zone].append(["Setting", effect, "to:",
                                            *color[c_used], '@ timing level', time])
            elif effect == 'ripple':
                # Effects that use 1 color and a refresh rate
                if len(arg) == 0:
                    refresh = razer_constants.RIPPLE_REFRESH_RATE
                else:
                    refresh = float(arg[0])
                rgb = color[c_used]
                if getattr(prop, effect)(*rgb, refresh) and args.verbose:
                    debug_msg[zone].append(["Setting", effect, "to:", rgb])
            elif effect == 'ripple_random':
                if len(arg) == 0:
                    refresh = razer_constants.RIPPLE_REFRESH_RATE
                else:
                    refresh = float(arg[0])
                if getattr(prop, effect)(refresh) and args.verbose:
                    debug_msg[zone].append(["Setting to", effect])
            elif effect == 'starlight_single':
                # These are just numbers 1-3
                #time = [razer_constants.STARLIGHT_FAST, razer_constants.STARLIGHT_NORMAL, razer_constants.STARLIGHT_SLOW]
                if len(arg) == 0:
                    time = util.randint(1, 3)
                else:
                    time = int(arg[0])
                if getattr(prop, effect)(*color[c_used], time) and args.verbose:
                    debug_msg[zone].append(["Setting", effect, "to:",
                                            *color[c_used], '@ timing level', time])
            elif effect == 'starlight_dual':
                # These are just numbers 1-3
                #time = [razer_constants.STARLIGHT_FAST, razer_constants.STARLIGHT_NORMAL, razer_constants.STARLIGHT_SLOW]
                if len(arg) == 0:
                    time = util.randint(1, 3)
                else:
                    time = int(arg[0])
                if getattr(prop, effect)(*color[c_used], *color[c_used+1], time) and args.verbose:
                    debug_msg[zone].append(["Setting", effect, " @ timing level", time,
                                            "to:\n         [", *color[c_used], ']\n         [', *color[c_used+1]])
            elif effect == 'starlight_random':
                if len(arg) == 0:
                    time = util.randint(1, 3)
                else:
                    time = int(arg[0])
                if getattr(prop, effect)(time) and args.verbose:
                    debug_msg[zone].append(
                        ["Setting", effect, '@ timing level', time])
            elif effect == 'wave':
                # These are just numbers 1-2
                #direction=[razer_constants.WAVE_LEFT, razer_constants.WAVE_RIGHT]
                if len(arg) == 0:
                    direction = util.randint(1, 2)
                else:
                    direction = int(arg[0])
                if getattr(prop, effect)(direction) and args.verbose:
                    debug_msg[zone].append(
                        ["Setting", effect, ' in direction', direction])
            elif effect == 'brightness':
                if len(arg) == 0:
                    b = 100
                else:
                    b = int(arg[0])
                prop.brightness = b
                if args.verbose:
                    debug_msg[zone].append(["Setting", effect, 'to', b])
            elif effect == 'active':
                if len(arg) == 0:
                    b = True
                else:
                    b = bool(arg[0])
                prop.active = b
                if args.verbose:
                    debug_msg[zone].append(["Setting", effect, 'to', b])
            elif effect == 'multicolor':
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
                            prop.advanced.matrix.set(
                                row, col, colors_to_dist[counter % len(colors_to_dist)])
                            counter += 1
                    # prop.advanced.draw_fb_or()
                    prop.advanced.draw()
                    if args.verbose:
                        debug_msg[zone].append(
                            ["Setting", effect, "\n        ", colors_to_dist])
                except (AssertionError, ValueError) as e:
                    if args.verbose:
                        debug_msg[zone].append(["Warning:", str(e)])
            else:
                debug_msg[zone].append(
                    ["Looks like someone forget to program a action for", effect, "after adding it to the settings file"])

        c_used += used
        i += 1
    if args.verbose:
        for i in debug_msg:
            print('   '+i+':')
            for x in debug_msg[i]:
                print('     ', *x)
    # Save used settings for this device to a file
    if og_color_len == 0:
        color = []
    util.write_settings_to_file(device, effects, color, zones=zones)


def set_effect_to_all_devices(device_manager, input_effects, color, zones):
    """ Set one effect to all connected devices, if they support that effect """

    # Iterate over each device and set the effect
    for device in device_manager.devices:
        # If -d argument is set, only set those devices
        if (args.device and (device.name in args.device or device.serial in args.device)) or (not args.device):
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

    parser.add_argument("--battery", nargs="+",
                        help="set low threshold and/or idle delay"
                        " (use print as a value to show it)",
                        action="store")

    parser.add_argument("-l", "--list_devices",
                        help="list available devices, settings, and their supported capabilities/effects",
                        action="store_true")

    parser.add_argument("-ll", "--list_devices_long",
                        help="list available devices settings, and list their supported capabilities/effects",
                        action="store_true")

    parser.add_argument("-ls", "--list_devices_short",
                        help="list available devices and their settings",
                        action="store_true")

    parser.add_argument("--sync",
                        help="sync lighting effects to all supported "
                        "Razer products",
                        action="store_true")

    parser.add_argument("--restore",
                        help="Load last used settings",
                        action="store_true")

    parser.add_argument("--version",
                        help="Print version number",
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
        return util.print_manual(args.manual)

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
        color = []
        if args.color:
            color = parse_color(args.color)
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

        set_effect_to_all_devices(device_manager, effects, color, zones)
    if args.restore:
        util.load_settings_from_file(args.verbose)

    if args.dpi:
        set_dpi(device_manager)

    if args.poll:
        set_poll_rate(device_manager)

    if args.battery:
        set_battery(device_manager)

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

    if args.list_devices or args.list_devices_long or args.list_devices_short:
        list_devices(device_manager)

    if args.version:
        print("razer-cli:", __version__)
        print("   Installed in:",
              util.os.path.dirname(util.os.path.realpath(__file__)))
        print("python3-openrazer:", device_manager.version)
        print("openrazer-daemon:", device_manager.daemon_version)


if __name__ == "__main__":
    """ This is executed when run from the command line - obsolete """

    main()
