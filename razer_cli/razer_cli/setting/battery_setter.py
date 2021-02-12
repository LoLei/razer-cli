from argparse import Namespace

from razer_cli.razer_cli import util


def set_battery(device_manager, args: Namespace):
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
                        if args.battery[i] == "low" and stop > i + 1:
                            bat['low'] = int(args.battery[i + 1])
                            device.set_low_battery_threshold(bat['low'])
                            if args.verbose:
                                print(device.name, 'low battery =',
                                      device.get_low_battery_threshold(), '%')
                        elif args.battery[i] == "idle" and stop > i + 1:
                            bat['idle'] = int(args.battery[i + 1])
                            device.set_idle_time(bat['idle'])
                            if args.verbose:
                                print(device.name, 'idle delay =',
                                      device.get_idle_time(), 'seconds')
                        i += 1
                    # Save used settings for this device to a file
                    util.write_settings_to_file(device, battery=bat)
            else:
                print('Does', device.name, 'have a battery?')
