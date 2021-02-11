CACHE_DIR = ".cache/razer-cli"
CACHE_FILE = "razer-cli-settings.json"

# Effects that do not use RGB input
COLOR_EFFECTS = [
    'breath_single',
    'breath_dual',
    'breath_triple',
    'blinking',
    'reactive',
    'ripple',
    'pulsate',
    'starlight_single',
    'starlight_dual',
    'static'
]

# Effects that have RGB input
COLORLESS_EFFECTS = [
    'active',
    'none',
    'brightness',
    'breath_random',
    'ripple_random',
    'starlight_random',
    'spectrum',
    'wave',
]

# Effect names known to exist in the driver (COLOR_EFFECTS + COLORLESS_EFFECTS)
EFFECTS = sorted([
    *COLOR_EFFECTS,
    *COLORLESS_EFFECTS
])

# These effects are not built-in the driver
CUSTOM_EFFECTS = [
    # Multiple colors - Either no additional argument and a random color is
    # chosen for each key, or colors can be supplied which are then evenly
    # distributed, for example razer-cli -e multicolor,3 -c ff0000 00ff00
    # 0000ff
    'multicolor'
]

ALL_EFFECTS = [
    *EFFECTS,
    *CUSTOM_EFFECTS,
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
