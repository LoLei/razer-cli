from razer_cli.razer_cli import settings


def reset_device_effect(device):
    # Currently not used, disabled in set_effect_to_device
    # Set the effect to static, requires colors in 0-255 range
    device.fx.static(0, 0, 0)
    for i in settings.ZONES:
        ele = getattr(device.fx.misc, i)
        if ele:
            ele.static(0, 0, 0)
