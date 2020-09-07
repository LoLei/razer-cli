CACHE_DIR = ".cache/razer-cli"
CACHE_FILE = "razer-cli-settings.json"

EFFECTS = [
        'breath_dual',
        'breath_random',
        'breath_single',
        'breath_triple',
        'left_breath_single',
        'left_reactive',
        'left_static',
        'logo_breath_single',
        'logo_reactive',
        'logo_static',
        'pulsate',
        'reactive',
        'right_breath_single',
        'right_reactive',
        'right_static',
        'ripple',
        'ripple_random',
        'scroll_breath_single',
        'scroll_reactive',
        'scroll_static',
        'spectrum',
        'starlight_dual',
        'starlight_random',
        'startlight_single',
        'static',
        'wave',
]

# These effects are not built-in the driver
CUSTOM_EFFECTS = [
        # Multiple colors - Either no additional argument and a random color is
        # chosen for each key, or colors can be supplied which are then evenly
        # distributed, for example razer-cli -e multicolor ff0000 00ff00
        # 0000ff
        'multicolor'
]
