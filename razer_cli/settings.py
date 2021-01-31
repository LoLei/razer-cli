CACHE_DIR = ".cache/razer-cli"
CACHE_FILE = "razer-cli-settings.json"

# Effect names known to exist in the driver
EFFECTS = [
    'none',
    'brightness',
    'breath_single',
    'breath_dual',
    'breath_triple',
    'breath_random',
    'reactive',
    'ripple',
    'ripple_random',
    'spectrum',
    'starlight_single',
    'starlight_dual',
    'starlight_random',
    'static',
    'wave'
]

# These effects are not built-in the driver
CUSTOM_EFFECTS = [
    # Multiple colors - Either no additional argument and a random color is
    # chosen for each key, or colors can be supplied which are then evenly
    # distributed, for example razer-cli -e multicolor,3 -c ff0000 00ff00
    # 0000ff
    'multicolor'
]

# These are the known lighting zones built into the driver, generic is a custom
# name for the entire device and not a specific zone
ZONES = [
    'generic',
    'logo',
    'scroll_wheel',
    'left',
    'right',
    'backlight'
]
