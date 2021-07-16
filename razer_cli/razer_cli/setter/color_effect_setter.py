from openrazer.client import constants as razer_constants

from razer_cli.razer_cli import settings, util
from razer_cli.razer_cli.parser.color_parser import parse_color
from razer_cli.razer_cli.setter.setter import Setter


class ColorEffectSetter(Setter):

    def set(self, **kwargs):
        # def set_effect_to_all_devices(device_manager, input_effects, color, zones, self.args: Namespace):
        """ Set one effect to all connected devices, if they support that effect """

        # Iterate over each device and set the effect
        for device in self.device_manager.devices:
            # If -d argument is set, only set those devices
            if (self.args.device and (device.name in self.args.device or device.serial in self.args.device)) or \
                    (not self.args.device):
                if self.args.verbose:
                    print('Setting effects for {}:'.format(device.name))
                self.set_effect_to_device(device, **kwargs)

    def set_effect_to_device(self, device, effects, color, zones):
        # Known Effects: advanced, breath_dual, breath_random, breath_single,
        #    breath_triple, blinking, none, reactive, ripple, ripple_random,
        #    pulsate, spectrum, starlight_dual, starlight_random,
        #    starlight_single, static, wave

        if self.args.verbose:
            debug_msg = {}
        og_color_len = len(color)
        c_used = 0
        i = 0
        stop = len(zones)
        if len(effects) < stop:
            stop = len(effects)
            if self.args.verbose:
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
                if self.args.verbose:
                    if zone not in debug_msg:
                        debug_msg[zone] = []
                if not util.rgb_support(device, zone, effect):
                    if self.args.verbose:
                        if util.rgb_support(device, zone):
                            debug_msg[zone].append(['Does not support', effect])
                        else:
                            debug_msg[zone].append([zone, 'is not supported'])
                    continue
                if zone == 'generic':
                    prop = device.fx
                else:
                    if zone in ["scroll", "wheel"]:
                        if self.args.verbose:
                            debug_msg[zone].append(
                                ['not valid, assuming scroll_wheel'])
                        zone = "scroll_wheel"
                        zones[i].append(zone)
                        continue
                    prop = getattr(device.fx.misc, zone)
                if og_color_len == 0 and effect not in settings.COLORLESS_EFFECTS and not (
                        effect == 'multicolor' and (len(arg) == 0 or arg[0] == '0')):
                    # Lets get default colors
                    # We can skip this if the effect does not need colors
                    # * multicolor does NOT use consume colors if set to 0 (default)
                    try:
                        # hasattr will error anyway if does not work, no point testing it
                        color = parse_color(
                            util.bytes_array_to_hex_array(getattr(prop, 'colors')), self.args)
                    except:
                        color = [util.get_x_color(verbose=self.args.verbose)]
                    c_used = 0
                    if self.args.verbose:
                        debug_msg[zone].append(["No color given, using:", color])
                if effect not in settings.ALL_EFFECTS:
                    debug_msg[zone].append(
                        ["Sorry", effect, "is supported by the hardware, but this software does not\n",
                         "         Consider makeing a bug report:\n",
                         "            https://github.com/LoLei/razer-cli/issues"])
                    continue
                # Prep colors
                used = 0
                if effect not in settings.COLORLESS_EFFECTS:
                    # Custom effects do this in there own block
                    used = 1
                    if effect == 'breath_triple':
                        used = 3
                    elif effect in ['breath_dual', 'starlight_dual']:
                        used = 2
                    while len(color) < c_used + used:
                        color.append(util.get_random_color_rgb())
                    # Do I really need this message?
                    # if self.args.verbose:
                    #    debug_msg[zone].append(["Using color(s):",
                    #                           [*color[c_used:c_used+used]],
                    #                           "\n         from:",color])
                # Set Effect
                if effect in ['none', 'breath_random', 'spectrum']:
                    # Effects that use no parameters
                    if getattr(prop, effect)() and self.args.verbose:
                        debug_msg[zone].append(["Setting to", effect])
                elif effect in ['static', 'breath_single', 'blinking', 'pulsate']:
                    # Effects that use 1 color
                    rgb = color[c_used]
                    if getattr(prop, effect)(*rgb) and self.args.verbose:
                        debug_msg[zone].append(["Setting", effect, "to:", *rgb])
                elif effect == 'breath_dual':
                    # Effects that use 2 colors
                    rgb = color[c_used]
                    rgb2 = color[c_used + 1]
                    if getattr(prop, effect)(*rgb, *rgb2) and self.args.verbose:
                        debug_msg[zone].append(["Setting", effect,
                                                "to:\n         [", *rgb, ']\n         [', *rgb2, ']'])
                elif effect == 'breath_triple':
                    # Effects that use 3 colors
                    rgb = color[c_used]
                    rgb2 = color[c_used + 1]
                    rgb3 = color[c_used + 2]
                    if getattr(prop, effect)(*rgb, *rgb2, *rgb3) and self.args.verbose:
                        debug_msg[zone].append(["Setting", effect,
                                                "to:\n         [", *rgb, ']\n         [', *rgb2, ']\n         [', *rgb3,
                                                ']'])
                elif effect == 'reactive':
                    # These are just numbers 1-4
                    # time = [razer_constants.REACTIVE_500MS, razer_constants.REACTIVE_1000MS,
                    # razer_constants.REACTIVE_1500MS, razer_constants.REACTIVE_2000MS]
                    if len(arg) == 0:
                        time = util.randint(1, 4)
                    else:
                        time = int(arg[0])
                    if getattr(prop, effect)(*color[c_used], time) and self.args.verbose:
                        debug_msg[zone].append(["Setting", effect, "to:",
                                                *color[c_used], '@ timing level', time])
                elif effect == 'ripple':
                    # Effects that use 1 color and a refresh rate
                    if len(arg) == 0:
                        refresh = razer_constants.RIPPLE_REFRESH_RATE
                    else:
                        refresh = float(arg[0])
                    rgb = color[c_used]
                    if getattr(prop, effect)(*rgb, refresh) and self.args.verbose:
                        debug_msg[zone].append(["Setting", effect, "to:", rgb])
                elif effect == 'ripple_random':
                    if len(arg) == 0:
                        refresh = razer_constants.RIPPLE_REFRESH_RATE
                    else:
                        refresh = float(arg[0])
                    if getattr(prop, effect)(refresh) and self.args.verbose:
                        debug_msg[zone].append(["Setting to", effect])
                elif effect == 'starlight_single':
                    # These are just numbers 1-3
                    # time = [razer_constants.STARLIGHT_FAST, razer_constants.STARLIGHT_NORMAL,
                    # razer_constants.STARLIGHT_SLOW]
                    if len(arg) == 0:
                        time = util.randint(1, 3)
                    else:
                        time = int(arg[0])
                    if getattr(prop, effect)(*color[c_used], time) and self.args.verbose:
                        debug_msg[zone].append(["Setting", effect, "to:",
                                                *color[c_used], '@ timing level', time])
                elif effect == 'starlight_dual':
                    # These are just numbers 1-3
                    # time = [razer_constants.STARLIGHT_FAST, razer_constants.STARLIGHT_NORMAL,
                    # razer_constants.STARLIGHT_SLOW]
                    if len(arg) == 0:
                        time = util.randint(1, 3)
                    else:
                        time = int(arg[0])
                    if getattr(prop, effect)(*color[c_used], *color[c_used + 1], time) and self.args.verbose:
                        debug_msg[zone].append(["Setting", effect, " @ timing level", time,
                                                "to:\n         [", *color[c_used], ']\n         [', *color[c_used + 1]])
                elif effect == 'starlight_random':
                    if len(arg) == 0:
                        time = util.randint(1, 3)
                    else:
                        time = int(arg[0])
                    if getattr(prop, effect)(time) and self.args.verbose:
                        debug_msg[zone].append(
                            ["Setting", effect, '@ timing level', time])
                elif effect == 'wave':
                    # These are just numbers 1-2
                    # direction=[razer_constants.WAVE_LEFT, razer_constants.WAVE_RIGHT]
                    if len(arg) == 0:
                        direction = util.randint(1, 2)
                    else:
                        direction = int(arg[0])
                    if getattr(prop, effect)(direction) and self.args.verbose:
                        debug_msg[zone].append(
                            ["Setting", effect, ' in direction', direction])
                elif effect == 'brightness':
                    if len(arg) == 0:
                        b = 100
                    else:
                        b = int(arg[0])
                    prop.brightness = b
                    if self.args.verbose:
                        debug_msg[zone].append(["Setting", effect, 'to', b])
                elif effect == 'active':
                    if len(arg) == 0:
                        b = True
                    else:
                        b = bool(arg[0])
                    prop.active = b
                    if self.args.verbose:
                        debug_msg[zone].append(["Setting", effect, 'to', b])
                elif effect == 'multicolor':
                    xpalette = False
                    if len(arg) > 0:
                        try:
                            # This should be renamed from 'used'
                            # Someone contributed this so I CBA'd to change it
                            used = int(arg[0])
                        except ValueError:
                            used = 0
                            xpalette = True
                    else:
                        used = 0
                    while len(color) < c_used + used:
                        color.append(util.get_random_color_rgb())
                    cols = prop.advanced.cols
                    rows = prop.advanced.rows
                    if used == 0:
                        if xpalette:
                            colors_to_dist = util.get_x_colors(verbose=self.args.verbose)
                        else:
                            colors_to_dist = [
                                util.get_random_color_rgb() for _ in range(cols * rows)]
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
                        if self.args.verbose:
                            debug_msg[zone].append(
                                ["Setting", effect, "\n        ", colors_to_dist])
                    except (AssertionError, ValueError) as e:
                        if self.args.verbose:
                            debug_msg[zone].append(["Warning:", str(e)])
                else:
                    debug_msg[zone].append(
                        ["Looks like someone forget to program a action for", effect,
                         "after adding it to the settings file"])

            c_used += used
            i += 1
        if self.args.verbose:
            for i in debug_msg:
                print('   ' + i + ':')
                for x in debug_msg[i]:
                    print('     ', *x)
        # Save used settings for this device to a file
        if og_color_len == 0:
            color = []
        util.write_settings_to_file(device, effects, color, zones=zones)
