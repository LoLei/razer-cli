from razer_cli.razer_cli.handler.Handler import Handler
from razer_cli.razer_cli.setter.brightness_setter import set_brightness


class BrightnessHandler(Handler):
    def handle(self):
        i = len(self.args.brightness)
        if i == 1 and self.args.brightness[0].isnumeric():
            self.args.brightness = {"all": self.args.brightness[0]}
            set_brightness(self.device_manager, self.args)
        elif i % 2 == 0:
            # Even number of arguments
            brightness = {}
            i = i - 1
            while i > -1:
                name = self.args.brightness[i - 1]
                value = self.args.brightness[i]
                if self.args.brightness[i].isnumeric():
                    brightness[name] = value
                else:
                    print('Warning:', value, 'is not a number for',
                          name, '[Skipping]')
                i = i - 2
            self.args.brightness = brightness
            set_brightness(self.device_manager, self.args)
        else:
            print("Invalid brightness input, see `razer-cli --manual brightness'")
