from argparse import Namespace

from razer_cli.razer_cli import util


def set_dpi(device_manager, args: Namespace):
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
