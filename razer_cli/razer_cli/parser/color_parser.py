from argparse import Namespace

from razer_cli.razer_cli import util


def parse_color(color, args: Namespace):
    """ Set the color either from the input argument or use a fallback color """

    RGB = []

    if (color):
        # Set colors from input argument
        stop = len(color)
        i = 0
        while i < stop:
            if len(color[i]) > 3 or color[i] in ['x', 'X']:
                if not len(color[i]) in [1, 6]:
                    print('color', len(RGB) + 1,
                          '(', color[i], ') looks to have a typo')
                RGB.append(parse_color_argument([color[i]], args))
                i += 1
            elif stop > i + 2:
                if len(color[i]) > 3 or len(color[i + 1]) > 3 or len(color[i + 2]) > 3:
                    print('color', len(
                        RGB) + 1, '(', color[i], color[i + 1], color[i + 2], ') looks to have a typo')
                rgb = [color[i], color[i + 1], color[i + 2]]
                RGB.append(parse_color_argument(rgb, args))
                i += 3
            else:
                print("Unexpected arguments for color")
                break

    else:
        # Use X colors as fallback if no color argument is set
        # TODO: Maybe also add argument to pull colors from
        # ~/.cache/wal.colors.jason
        RGB.append(util.get_x_color(args.verbose))

    return RGB


def parse_color_argument(color, args: Namespace):
    if len(color) == 1:
        # Hex: Just one input argument or key word
        rgb = color[0].lower()
        if rgb == "random":
            rgb = util.get_random_color_rgb()
        elif rgb == "x":
            rgb = util.get_x_color(args.verbose)
        else:
            rgb = util.hex_to_decimal(rgb)
    else:
        if len(color) == 3:
            # RGB: Three base10 input arguments
            rgb = []
            for i in color:
                if i.lower() == "rng":
                    rgb.append(util.randint(0, 255))
                else:
                    rgb.append(int(i))
        else:
            print("Unknown color input:", color)
            rgb = util.get_random_color_rgb()
    return rgb
