from razer_cli import settings
import os
import json
from random import randint


def hex_to_decimal(hex_color):
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return [r, g, b]


def bytes_array_to_hex_array(b):
    c_str = b.hex()
    colors = []
    stop = len(c_str)
    i = 0
    while i < stop:
        colors.append(c_str[i:i+6].upper())
        i += 6
    return colors


def get_random_color_rgb():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)

    return [r, g, b]


def rgb_support(device, zone=False, effect=False):
    prop = ["lighting"]
    if not device.capabilities[prop[0]]:
        # A Razer product without RGB? Does such a thing exist?
        return False
    if zone in ['scroll_wheel', 'wheel'] and not prop[0]+'_'+zone in device.capabilities:
        prop.append('scroll')
    elif zone and not zone == 'generic':
        prop.append(zone)
    if effect == 'advanced' or effect in settings.CUSTOM_EFFECTS:
        prop.append('led_matrix')
    elif effect:
        prop.append(effect)
    prop = '_'.join(prop)
    if prop in device.capabilities and device.capabilities[prop]:
        return True
    return False


def load_settings_from_file(verbose):
    home_dir = os.path.expanduser("~")
    dir_name = settings.CACHE_DIR
    file_name = settings.CACHE_FILE
    path_and_file = os.path.join(home_dir, dir_name, file_name)
    if verbose:
        print('file:', path_and_file)
    if os.path.isfile(path_and_file):
        print("Feature incomplete, here are the command(s) to restore the settings:")
        with open(path_and_file, 'r') as file:
            data = json.load(file)
        i = len(data)-1
        while i > -1:
            opts = "-d '"+data[i]['device_name']+"'"
            if data[i].get('color'):
                opts += " -c"
                for x in data[i]['color']:
                    rgb = 0
                    while rgb < 3:
                        opts += " "+str(x[rgb])
                        rgb += 1
            if data[i].get('zones'):
                opts += " -z"
                for x in data[i]['zones']:
                    opts += " "+str(','.join(x))
            if data[i].get('dpi'):
                opts += " --dpi "+str(data[i]['dpi'])
            if data[i].get('poll'):
                opts += " --poll "+str(data[i]['poll'])
            if data[i].get('effect'):
                opts += " -e "+str(data[i]['effect'])
            if data[i].get('brightness'):
                opts += " -b"
                for x in data[i]['brightness']:
                    opts += " "+x+" "+str(data[i]['brightness'][x])
            if data[i].get('battery'):
                opts += " --battery"
                for x in data[i]['battery']:
                    opts += " "+x+" "+str(data[i]['battery'][x])

            print('   ', 'razer-cli', opts)
            i -= 1

    else:
        print('There is no settings file')


def write_settings_to_file(device, effect=[], color="", dpi="", brightness={}, poll="", zones="", battery={}):
    """ Save settings to a file for possible later retrieval """

    home_dir = os.path.expanduser("~")
    dir_name = settings.CACHE_DIR
    file_name = settings.CACHE_FILE
    path_and_file = os.path.join(home_dir, dir_name, file_name)

    # Handle non-existing file
    if not os.path.isfile(path_and_file):
        os.makedirs(os.path.dirname(path_and_file), exist_ok=True)
        print("creating path and file")
        a = []
        with open(path_and_file, mode='w') as file:
            json.dump(a, file)

    # Check if there already exists an entry for this device, if yes update it
    found_existing_settings = False
    with open(path_and_file, 'r') as file:
        json_data = json.load(file)
        for item in json_data:
            if (item['device_name'] == device.name):
                found_existing_settings = True
                if (color != ""):
                    item['color'] = color
                if (zones != ""):
                    item['zones'] = zones
                if len(effect) > 0:
                    item['effect'] = ' '.join(effect)
                if (dpi != ""):
                    item['dpi'] = dpi
                if (poll != ""):
                    item['poll'] = poll
                if len(brightness) > 0:
                    if not hasattr(item,'brightness'):
                        item['brightness']={}
                    for i in brightness:
                        item['brightness'][i] = brightness[i]
                if len(battery) > 0:
                    if not hasattr(item,'battery'):
                        item['battery']={}
                    for i in battery:
                        item['battery'][i] = battery[i]

    # Update existing entry
    if found_existing_settings:
        with open(path_and_file, 'w') as file:
            json.dump(json_data, file, indent=2)
    # If no existing entry was found, append a new entry
    else:
        print("Adding new settings entry")
        used_settings = {}
        used_settings['device_name'] = device.name
        if (color != ""):
            used_settings['color'] = color
        if (zones != ""):
            used_settings['zones'] = zones
        if len(effect) > 0:
            used_settings['effect'] = ' '.join(effect)
        if (dpi != ""):
            used_settings['dpi'] = dpi
        if (poll != ""):
            used_settings['poll'] = poll
        if len(brightness) > 0:
            used_settings['brightness'] = brightness
        if len(battery) > 0:
            used_settings['battery'] = battery
        with open(path_and_file, mode='w') as file:
            json_data.append(used_settings)
            json.dump(json_data, file, indent=2)


def print_manual(man):
    d_path = os.path.dirname(os.path.realpath(__file__))+'/man_pages'
    if len(man) == 0:
        return print("Manual entries exist for:", ', '.join(sorted(os.listdir(d_path))))
    for i in man:
        f_path = d_path+'/'+i
        if os.path.isfile(f_path):
            with open(f_path, "r") as f:
                print("Manual Entry for --{}:".format(i))
                print(f.read())
        else:
            print("No manual entries exist for", i,
                  "try:\n  ", ', '.join(sorted(os.listdir(d_path))))
