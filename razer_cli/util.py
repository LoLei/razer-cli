from razer_cli import settings
import os
import json
import random


def hex_to_decimal(hex_color):
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return r, g, b


def get_random_color_rgb():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return r, g, b


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
            if data[i]['color']:
                opts += " -c"
                for x in data[i]['color']:
                    rgb = 0
                    while rgb < 3:
                        opts += " "+str(x[rgb])
                        rgb += 1
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

            print('   ', 'razer-cli', opts)
            i -= 1

    else:
        print('There is no settings file')


def write_settings_to_file(device, effect="", color="", dpi="", brightness="", poll=""):
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
                if (effect != ""):
                    item['effect'] = effect
                if (dpi != ""):
                    item['dpi'] = dpi
                if (poll != ""):
                    item['poll'] = poll
                if (brightness != ""):
                    for i in brightness:
                        item['brightness'][i] = brightness[i]

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
        if (effect != ""):
            used_settings['effect'] = effect
        if (dpi != ""):
            used_settings['dpi'] = dpi
        if (poll != ""):
            used_settings['poll'] = poll
        if (brightness != ""):
            used_settings['brightness'] = brightness
        with open(path_and_file, mode='w') as file:
            json_data.append(used_settings)
            json.dump(json_data, file, indent=2)
