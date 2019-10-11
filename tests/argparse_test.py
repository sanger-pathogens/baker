import argparse
import unittest
from bakerlib.argument_parsing import ArgumentParserBuilder


class TestDecorateParser(unittest.TestCase):

    def setUp(self):
        self.under_test = ArgumentParserBuilder.new_instance(
            lambda: ErrorRaisingArgumentParser()).with_decorating(mock_decorating).build()

    def test_parser_single_directory(self):
        args = self.under_test.parse_args(
            ['decorate', '--templates', 'templates', '--output', 'out', '--input', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', template_dir='templates', output_dir='out', func=mock_decorating))

    def test_parser_short_options(self):
        args = self.under_test.parse_args(
            ['decorate', '-t', 'templates', '-o', 'out', '-i', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', template_dir='templates', output_dir='out', func=mock_decorating))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', '--templates', 'templates', '--output', 'out'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --input/-i')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', '--templates', 'templates', '--input', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', '--output', 'out', '--input', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --templates/-t')


def mock_decorating():
    pass


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
