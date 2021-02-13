from argparse import Namespace

from razer_cli.razer_cli import settings, util


def set_brightness(device_manager, args: Namespace):
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
                        print('        Setting lighting_' + i +
                              '_brightness to', brightness[i])
                    val = int(brightness[i])
                    if i == 'scroll':
                        i = 'scroll_wheel'
                    getattr(device.fx.misc, i).brightness = val
                elif args.verbose:
                    print('        Device does not support lighting_' +
                          i + '_brightness')
            # Save used settings for this device to a file
            util.write_settings_to_file(device, brightness=brightness)
