from argparse import Namespace

from razer_cli.razer_cli import util


def set_poll_rate(device_manager, args: Namespace):
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
