from argparse import Namespace

from razer_cli.razer_cli import util
from razer_cli.razer_cli.setter.setter import Setter


class BatterySetter(Setter):

    def set(self):
        for device in self.device_manager.devices:
            if (self.args.device and (device.name in self.args.device or device.serial in self.args.device)) or (not self.args.device):
                if device.has("battery"):
                    if len(self.args.battery) < 2:
                        print(device.name, 'battery:')
                        print("   charge:", device.battery_level)
                        print("   charging:", device.is_charging)
                        if device.has('get_low_battery_threshold'):
                            print("   low threshold:",
                                device.get_low_battery_threshold(), '%')
                        if device.has('get_idle_time'):
                            print("   idle delay", device.get_idle_time(), 'seconds')
                    else:
                        i = 0
                        stop = len(self.args.battery)
                        bat = {}
                        while i < stop:
                            if self.args.battery[i] == "low" and stop > i + 1:
                                bat['low'] = int(self.args.battery[i + 1])
                                if device.has("set_low_battery_threshold"):
                                    device.set_low_battery_threshold(bat['low'])
                                if self.args.verbose and device.has("get_low_battery_threshold"):
                                    print(device.name, 'low battery =',
                                          device.get_low_battery_threshold(), '%')
                            elif self.args.battery[i] == "idle" and stop > i + 1:
                                bat['idle'] = int(self.args.battery[i + 1])
                                if device.has("set_idle_time"):
                                    device.set_idle_time(bat['idle'])
                                if self.args.verbose and device.has("get_idle_time"):
                                    print(device.name, 'idle delay =',
                                          device.get_idle_time(), 'seconds')
                            i += 1
                        # Save used settings for this device to a file
                        util.write_settings_to_file(device, battery=bat)
                else:
                    print('Does', device.name, 'have a battery?')
