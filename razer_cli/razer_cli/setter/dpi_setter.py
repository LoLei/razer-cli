from argparse import Namespace

from razer_cli.razer_cli import util
from razer_cli.razer_cli.setter.setter import Setter


class DpiSetter(Setter):
    def set(self):
        # Iterate over each device and set DPI
        for device in self.device_manager.devices:
            # If -d argument is set, only set those devices
            if (self.args.device and (device.name in self.args.device or device.serial in self.args.device)) or (not self.args.device):
                if not device.has('dpi'):
                    if self.args.verbose:
                        print("Device {} is not have a DPI setter".format(device.name))
                elif self.args.dpi == "print":
                    dpi = device.dpi
                    if self.args.poll == "print":
                        if dpi[0] == dpi[1] or self.args.battery and len(self.args.battery) == 1:
                            print('DPI:', dpi[0])
                        else:
                            print('DPI:', *dpi)
                    else:
                        if dpi[0] == dpi[1]:
                            print(dpi[0])
                        else:
                            print(*dpi)
                else:
                    if self.args.verbose:
                        print("Setting DPI of device {} to {}".format(device.name,
                                                                      self.args.dpi))

                    # Actually set DPI
                    dpi = self.args.dpi.split(',')
                    if len(dpi) == 1:
                        dpi.append(int(dpi[0]))
                    device.dpi = (int(dpi[0]), int(dpi[1]))

                    # Save used settings for this device to a file
                    util.write_settings_to_file(device, dpi=self.args.dpi)
