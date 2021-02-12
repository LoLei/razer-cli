import unittest
from argparse import Namespace

from razer_cli.razer_cli.parsing.argument_parser import read_args


class TestArgumentParser(unittest.TestCase):
    def test_argparse_namespace(self):
        args: Namespace
        args = read_args(["-ls"])
        self.assertTrue(args.list_devices_short)

        # TODO: Test more arguments
        # TODO: Test more everything

    def test_function_namespace_annotation(self):
        # Just make sure it doesn't crash
        def function_with_namespace_args(args: Namespace) -> Namespace:
            return Namespace()
        function_with_namespace_args(Namespace())
