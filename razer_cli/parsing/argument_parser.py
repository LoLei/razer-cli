import argparse
import sys
from typing import List


def read_args(input_args: List[str]) -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    parser.add_argument("-man", "--manual", nargs="*",
                        help="Print help details for given feature(s)",
                        action="store")

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-d", "--device", nargs="+",
                        help="only affect these devices, same name as output "
                             "of -l")

    parser.add_argument("-a", "--automatic",
                        help="try to find colors and set them to all devices "
                             "without user arguments, uses X or pywal colors",
                        action="store_true")

    parser.add_argument("-e", "--effect",
                        help="set effect",
                        action="store",
                        nargs="+")

    parser.add_argument("-c", "--color", nargs="+",
                        help="choose color (default: X color1), use one argument "
                             "for hex, or three for base10 rgb")

    parser.add_argument("-z", "--zone", nargs="+",
                        dest='zones',
                        help="choose zone for color(s)")

    parser.add_argument("-b", "--brightness", nargs="+",
                        help="set brightness of device",
                        dest='brightness',
                        action="store")

    parser.add_argument("--dpi", help="set DPI of device"
                                      " (use print as a value to show it)",
                        action="store")

    parser.add_argument("--poll",
                        help="set polling rate of device"
                             " (use print as a value to show it)",
                        action="store")

    parser.add_argument("--battery", nargs="+",
                        help="set low threshold and/or idle delay"
                             " (use print as a value to show it)",
                        action="store")

    parser.add_argument("-l", "--list_devices",
                        help="list available devices, settings, and their supported capabilities/effects",
                        action="store_true")

    parser.add_argument("-ll", "--list_devices_long",
                        help="list available devices settings, and list their supported capabilities/effects",
                        action="store_true")

    parser.add_argument("-ls", "--list_devices_short",
                        help="list available devices and their settings",
                        action="store_true")

    parser.add_argument("--sync",
                        help="sync lighting effects to all supported "
                             "Razer products",
                        action="store_true")

    parser.add_argument("--restore",
                        help="Load last used settings",
                        action="store_true")

    parser.add_argument("--version",
                        help="Print version number",
                        action="store_true")

    if len(input_args) < 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args(input_args)
