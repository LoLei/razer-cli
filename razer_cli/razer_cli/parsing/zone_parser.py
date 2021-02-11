from razer_cli.razer_cli import settings


def parse_zones(zones_list):
    if not zones_list:
        return [settings.ZONES]
    zones = []
    stop = len(zones_list)
    i = 0
    while i < stop:
        if zones_list[i] == 'all':
            zones.append(settings.ZONES)
        else:
            zones.append(zones_list[i].split(','))
        i += 1
    return zones
