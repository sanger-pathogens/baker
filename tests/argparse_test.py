import argparse
import unittest
from bakerlib.argument_parsing import new_argument_parser


class TestDecorateParser(unittest.TestCase):

    def setUp(self):
        self.under_test = new_argument_parser(mock_decorating, mock_baking,
                                              factory=lambda: ErrorRaisingArgumentParser())

    def test_parser_multiple_directories(self):
        args = self.under_test.parse_args(
            ['decorate', '--templates', 'templates', '--output', 'out', 'dir1', 'dir2'])
        self.assertEqual(args, argparse.Namespace(
            input_dirs=['dir1', 'dir2'], template_dir='templates', output_dir='out', func=mock_decorating))

    def test_parser_single_directory(self):
        args = self.under_test.parse_args(
            ['decorate', '--templates', 'templates', '--output', 'out', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dirs=['dir1'], template_dir='templates', output_dir='out', func=mock_decorating))

    def test_parser_short_options(self):
        args = self.under_test.parse_args(
            ['decorate', '-t', 'templates', '-o', 'out', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dirs=['dir1'], template_dir='templates', output_dir='out', func=mock_decorating))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', '--templates', 'templates', '--output', 'out'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: directory')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', '--templates', 'templates', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(['decorate', '--output', 'out', 'dir'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --templates/-t')


class TestBakeParser(unittest.TestCase):

    def setUp(self):
        self.under_test = new_argument_parser(mock_decorating, mock_baking,
                                              factory=lambda: ErrorRaisingArgumentParser())

    def test_parser_multiple_directories(self):
        args = self.under_test.parse_args(
            ['bake', '--config', 'a_config', '--image', 'an_image', '--templates', 'templates', '--output', 'out', 'dir1', 'dir2'])
        self.assertEqual(args, argparse.Namespace(config = 'a_config', image='an_image', input_dirs=[
                         'dir1', 'dir2'], template_dir='templates', output_dir='out', func=mock_baking))

    def test_parser_single_directory(self):
        args = self.under_test.parse_args(
            ['bake', '--config', 'a_config', '--image', 'an_image', '--templates', 'templates', '--output', 'out', 'dir1'])
        self.assertEqual(args, argparse.Namespace(config = 'a_config', image='an_image', input_dirs=[
                         'dir1'], template_dir='templates', output_dir='out', func=mock_baking))

    def test_parser_short_options(self):
        args = self.under_test.parse_args(
            ['bake', '-c', 'a_config', '-i', 'an_image', '-t', 'templates', '-o', 'out', 'dir1'])
        self.assertEqual(args, argparse.Namespace(config = 'a_config', image='an_image', input_dirs=[
                         'dir1'], template_dir='templates', output_dir='out', func=mock_baking))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['bake', '--config', 'a_config', '--image', 'an_image', '--templates', 'templates', '--output', 'out'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: directory')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['bake', '--config', 'a_config', '--image', 'an_image', '--templates', 'templates', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['bake', '--config', 'a_config', '--image', 'an_image', '--output', 'out', 'dir'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --templates/-t')

    def test_image_is_not_mandatory(self):
        args = self.under_test.parse_args(
            ['bake', '--config', 'a_config', '--templates', 'templates', '--output', 'out', 'dir'])
        self.assertEqual(args, argparse.Namespace(config = 'a_config', image=None, input_dirs=[
                         'dir'], template_dir='templates', output_dir='out', func=mock_baking))

    def test_config_is_not_mandatory(self):
        args = self.under_test.parse_args(
            ['bake', '--image', 'an_image', '--templates', 'templates', '--output', 'out', 'dir'])
        self.assertEqual(args, argparse.Namespace(config = None, image='an_image', input_dirs=[
                         'dir'], template_dir='templates', output_dir='out', func=mock_baking))


def mock_decorating():
    pass


def mock_baking():
    pass


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
