import argparse
import unittest

from bakerlib.argument_parsing import ArgumentParserBuilder


class TestDecorateParser(unittest.TestCase):

    def setUp(self):
        self.target = 'catalog'
        self.under_test = ArgumentParserBuilder.new_instance(lambda: ErrorRaisingArgumentParser()) \
            .with_decorating(self.target, mock_function) \
            .build()

    def test_decorate(self):
        args = self.under_test.parse_args(
            ['decorate', self.target, '--template', 'template', '--output', 'out', '--input', 'dir1', '--file-mode',
             '0o755'])
        self.assertEqual(args,
                         argparse.Namespace(images=None, input_dir='dir1', template='template', output_format='out',
                                            file_mode=0o755, func=mock_function))

    def test_decorate_missing(self):
        args = self.under_test.parse_args(
            ['decorate', self.target, '--template', 'template', '--output', 'out', '--input', 'dir1', '--file-mode',
             '0o755', '--images', 'images'])
        self.assertEqual(args,
                         argparse.Namespace(images='images', input_dir='dir1', template='template', output_format='out',
                                            file_mode=0o755, func=mock_function))

    def test_decorate_short_options(self):
        args = self.under_test.parse_args(
            ['decorate', self.target, '-t', 'template', '-o', 'out', '-i', 'dir1', '-f', '0o755'])
        self.assertEqual(args,
                         argparse.Namespace(images=None, input_dir='dir1', template='template', output_format='out',
                                            file_mode=0o755, func=mock_function))

    def test_decorate_short_options_missing(self):
        args = self.under_test.parse_args(
            ['decorate', self.target, '-t', 'template', '-o', 'out', '-i', 'dir1', '-f', '0o755', '-m', 'images'])
        self.assertEqual(args,
                         argparse.Namespace(images='images', input_dir='dir1', template='template', output_format='out',
                                            file_mode=0o755, func=mock_function))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', self.target, '--template', 'template', '--output', 'out', '--file-mode', '0o755'])
        self.assertEqual(cm.exception.args[0], 'the following arguments are required: --input/-i')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', self.target, '--template', 'template', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', self.target, '--output', 'out', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(cm.exception.args[0], 'the following arguments are required: --template/-t')

    def test_fail_if_no_file_mode(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', self.target, '--template', 'template', '--output', 'out', '--input', 'dir1'])
        self.assertEqual(cm.exception.args[0], 'the following arguments are required: --file-mode/-f')

def mock_function():
    pass


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
