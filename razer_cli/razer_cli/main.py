#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lorenz Leitner"
__version__ = "2.0.1"
__license__ = "GPL-3.0"

import sys

from openrazer.client import DeviceManager

from razer_cli.razer_cli import util
from razer_cli.razer_cli.parser.argument_parser import read_args
from razer_cli.razer_cli.rc import RazerCli


def main() -> None:
    """ Main entry point of the app """
    args = read_args(sys.argv[1:])

    if args.manual is not None:
        return util.print_manual(args.manual)

    # Create a DeviceManager. This is used to get specific devices
    device_manager = DeviceManager()

    rc = RazerCli.init_create(device_manager, args, __version__)
    rc.run()


if __name__ == "__main__":
    """ This is executed when run from the command line - obsolete """

    main()
