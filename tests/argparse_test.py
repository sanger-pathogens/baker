import argparse
import unittest
from bakerlib.argument_parsing import new_argument_parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.under_test = new_argument_parser(mock_backing,
                                              factory=lambda: ErrorRaisingArgumentParser())

    def test_parser_multiple_directories(self):
        args = self.under_test.parse_args(
            ['decorate', '--templates', 'templates', '--output', 'out', 'dir1', 'dir2'])
        self.assertEqual(args, argparse.Namespace(
            input_dirs=['dir1', 'dir2'], template_dir='templates', output_dir='out', func=mock_backing))

    def test_parser_single_directory(self):
        args = self.under_test.parse_args(['decorate', '--templates', 'templates', '--output', 'out', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dirs=['dir1'], template_dir='templates', output_dir='out', func=mock_backing))

    def test_parser_short_options(self):
        args = self.under_test.parse_args(['decorate', '-t', 'templates', '-o', 'out', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dirs=['dir1'], template_dir='templates', output_dir='out', func=mock_backing))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(['decorate', '--templates', 'templates', '--output', 'out'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: directory')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(['decorate', '--templates', 'templates', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(['decorate','--output', 'out', 'dir'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --templates/-t')


def mock_backing():
    pass


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
