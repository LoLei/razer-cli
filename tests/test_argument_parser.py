import unittest
from argparse import Namespace

from razer_cli.parsing.argument_parser import read_args


class TestArgumentParser(unittest.TestCase):
    def test_argparse_namespace(self):
        args: Namespace
        args = read_args(["-ls"])
        self.assertTrue(args.list_devices_short)
