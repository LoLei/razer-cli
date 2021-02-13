from argparse import Namespace

from razer_cli.razer_cli import util
from razer_cli.razer_cli.setter.setter import Setter


class PollRateSetter(Setter):

    def set(self):
        # Iterate over each device and set Polling Rate
        for device in self.device_manager.devices:
            # If -d argument is set, only set those devices
            if (self.args.device and (device.name in self.args.device or device.serial in self.args.device)) or (not self.args.device):
                if device.has("poll_rate"):
                    if self.args.poll == "print":
                        if self.args.dpi == "print" or self.args.battery and len(self.args.battery) == 1:
                            print('poll_rate:', device.poll_rate)
                        else:
                            print(device.poll_rate)
                    else:
                        if self.args.verbose:
                            print(
                                "Setting polling rate of device {} to {}".format(
                                    device.name,
                                    self.args.poll))

                        # Actually set Polling Rate
                        device.poll_rate = int(self.args.poll)

                        # Save used settings for this device to a file
                        util.write_settings_to_file(device, poll=self.args.poll)
                else:
                    print("Device does not support setter the polling rate")
