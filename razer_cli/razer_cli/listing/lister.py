from argparse import Namespace

from razer_cli.razer_cli import settings, util


def list_devices(device_manager, args: Namespace):
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
                print(device.name + ':')
            else:
                print("unknown device:")
            if device.has('type'):
                print("   type:", device.type)
            # https://www.youtube.com/watch?v=rnZYEuqKGCo
            # if hasattr(device,'device_image'):
            #    print("   image url:", device.device_image)
            if device.has('dpi'):
                print("   DPI:", device.dpi)
                print("   max DPI:", device.max_dpi)
            if (device.has('available_dpi')):
                print("   available DPI:", device.available_dpi)
            if (device.has('dpi_stages')):
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

            print("   supported capabilities:" + start_str,
                  glue_str.join(capabilitity['supported']))
            if args.verbose:
                print("   unsupported capabilities:" + start_str,
                      glue_str.join(capabilitity['unsupported']))
            print()
