from razer_cli.razer_cli import util
from razer_cli.razer_cli.handler.handler import Handler
from razer_cli.razer_cli.parser.color_parser import parse_color
from razer_cli.razer_cli.parser.zone_parser import parse_zones
from razer_cli.razer_cli.setter.effect_setter import set_effect_to_all_devices


class ColorEffectHandler(Handler):
    def handle(self):
        color = []
        if self.args.color:
            color = parse_color(self.args.color, self.args)
        elif self.args.automatic:
            color = [util.get_x_color(self.args.verbose)]
        zones = parse_zones(self.args.zones)
        if not self.args.effect:
            effects = ['static']
            if self.args.automatic and not self.args.brightness and len(zones) == 1:
                effects.append('brightness')
        else:
            effects = self.args.effect

        stop = len(zones)
        if len(effects) == 1 and stop > 1:
            while len(effects) < stop:
                effects.append(effects[0])
        elif stop == 1 and len(effects) > 1:
            stop = len(effects)
            while len(zones) < stop:
                zones.append([*zones[0]])

        set_effect_to_all_devices(self.device_manager, effects, color, zones, self.args)
