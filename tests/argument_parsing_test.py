import argparse
import unittest

from bakerlib.argument_parsing import ArgumentParserBuilder


class TestDecorateFunctionParser(unittest.TestCase):

    def setUp(self):
        self.under_test = ArgumentParserBuilder.new_instance(lambda: ErrorRaisingArgumentParser()) \
            .with_function_decorating(mock_function) \
            .build()

    def test_decorate_function_single_directory(self):
        args = self.under_test.parse_args(
            ['decorate', 'function', '--template', 'template', '--output', 'out', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', template='template', output_dir='out', file_mode=0o755, func=mock_function))

    def test_decorate_function_short_options(self):
        args = self.under_test.parse_args(
            ['decorate', 'function', '-t', 'template', '-o', 'out', '-i', 'dir1', '-f', '0o755'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', template='template', output_dir='out', file_mode=0o755, func=mock_function))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'function', '--template', 'template', '--output', 'out', '--file-mode', '0o755'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --input/-i')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'function', '--template', 'template', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'function', '--output', 'out', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --template/-t')

    def test_fail_if_no_file_mode(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'function', '--template', 'template', '--output', 'out', '--input', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --file-mode/-f')


class TestDecorateSoftwareParser(unittest.TestCase):

    def setUp(self):
        self.under_test = ArgumentParserBuilder.new_instance(lambda: ErrorRaisingArgumentParser()) \
            .with_software_decorating(mock_function) \
            .build()

    def test_decorate(self):
        args = self.under_test.parse_args(
            ['decorate', 'software', '--template', 'template', '--output', 'out', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', template='template', output_dir='out', file_mode=0o755, func=mock_function))

    def test_decorate_short_options(self):
        args = self.under_test.parse_args(
            ['decorate', 'software', '-t', 'template', '-o', 'out', '-i', 'dir1', '-f', '0o755'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', template='template', output_dir='out', file_mode=0o755, func=mock_function))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'software', '--template', 'template', '--output', 'out', '--file-mode', '0o755'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --input/-i')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'software', '--template', 'template', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'software', '--output', 'out', '--input', 'dir1', '--file-mode', '0o755'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --template/-t')

    def test_fail_if_no_file_mode(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['decorate', 'software', '--template', 'template', '--output', 'out', '--input', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --file-mode/-f')


class TestSingularityCheckParser(unittest.TestCase):

    def setUp(self):
        self.under_test = ArgumentParserBuilder.new_instance(lambda: ErrorRaisingArgumentParser()) \
            .with_singularity_check(mock_function) \
            .build()

    def test_parser_single_directory(self):
        args = self.under_test.parse_args(
            ['singularity', 'check', '--output', 'out', '--input', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', output_dir='out', func=mock_function))

    def test_parser_short_options(self):
        args = self.under_test.parse_args(
            ['singularity', 'check', '-o', 'out', '-i', 'dir1'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', output_dir='out', func=mock_function))

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'check', '--output', 'out'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --input/-i')

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'check', '--input', 'dir1'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')


class TestSingularityBakeParser(unittest.TestCase):

    def setUp(self):
        self.under_test = ArgumentParserBuilder.new_instance(lambda: ErrorRaisingArgumentParser()) \
            .with_singularity_bake(mock_function) \
            .build()

    def test_parser_bake_missing(self):
        args = self.under_test.parse_args(
            ['singularity', 'bake', '--input', 'dir1', '--output', 'out', '--missing', '--config', 'config'])
        self.assertEqual(args, argparse.Namespace(
            missing=True, input_dir='dir1', output_dir='out', images=[], func=mock_function, config='config'))

    def test_parser_bake_image(self):
        args = self.under_test.parse_args(
            ['singularity', 'bake', '--input', 'dir1', '--output', 'out', '--image-name', 'image1', '--config',
             'config'])
        self.assertEqual(args, argparse.Namespace(
            missing=False, input_dir='dir1', output_dir='out', images=['image1'], func=mock_function, config='config'))

    def test_parser_bake_multiple_images(self):
        args = self.under_test.parse_args(
            ['singularity', 'bake', '--input', 'dir1', '--output', 'out', '--image-name', 'image1', '--image-name',
             'image2', '--config', 'config'])
        self.assertEqual(args, argparse.Namespace(
            missing=False, input_dir='dir1', output_dir='out', images=['image1', 'image2'], func=mock_function,
            config='config'))

    def test_parser_short_options_missing(self):
        args = self.under_test.parse_args(
            ['singularity', 'bake', '-i', 'dir1', '-o', 'out', '-m', '-c', 'config'])
        self.assertEqual(args, argparse.Namespace(
            missing=True, input_dir='dir1', output_dir='out', images=[], func=mock_function, config='config'))

    def test_parser_short_options_images(self):
        args = self.under_test.parse_args(
            ['singularity', 'bake', '-i', 'dir1', '-o', 'out', '-n', 'image1', '-n', 'image2', '-c', 'config'])
        self.assertEqual(args, argparse.Namespace(
            missing=False, input_dir='dir1', output_dir='out', images=['image1', 'image2'], func=mock_function,
            config='config'))

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'bake', '--input', 'dir1', '--missing', '--config', 'config'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'bake', '--output', 'out', '--missing', '--config', 'config'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --input/-i')

    def test_fail_if_no_image_and_no_missing(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'bake', '--input', 'dir1', '--output', 'out', '--config', 'config'])
        self.assertEqual(
            cm.exception.args[0], 'one of the arguments --missing/-m --image-name/-n is required')

    def test_fail_if_no_config(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'bake', '--input', 'dir1', '--output', 'out', '--missing'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --config/-c')


class TestSingularityLegacyBakeParser(unittest.TestCase):

    def setUp(self):
        self.under_test = ArgumentParserBuilder.new_instance(lambda: ErrorRaisingArgumentParser()) \
            .with_legacy_bake(mock_function) \
            .build()

    def test_parser_bake_image(self):
        args = self.under_test.parse_args(
            ['singularity', 'legacy-bake', '--input', 'dir1', '--output', 'out', '--image-name', 'image1',
             '--templates', 'templates'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', output_dir='out', images=['image1'], func=mock_function, template_dir='templates'))

    def test_parser_bake_multiple_images(self):
        args = self.under_test.parse_args(
            ['singularity', 'legacy-bake', '--input', 'dir1', '--output', 'out', '--image-name', 'image1',
             '--image-name', 'image2', '--templates', 'templates'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', output_dir='out', images=['image1', 'image2'], func=mock_function,
            template_dir='templates'))

    def test_parser_short_options_images(self):
        args = self.under_test.parse_args(
            ['singularity', 'legacy-bake', '-i', 'dir1', '-o', 'out', '-n', 'image1', '-n', 'image2', '-t',
             'templates'])
        self.assertEqual(args, argparse.Namespace(
            input_dir='dir1', output_dir='out', images=['image1', 'image2'], func=mock_function,
            template_dir='templates'))

    def test_fail_if_no_output_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'legacy-bake', '--input', 'dir1', '--image-name', 'image1', '--templates', 'templates'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --output/-o')

    def test_fail_if_no_template_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'legacy-bake', '--input', 'dir1', '--image-name', 'image1', '--output', 'out'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --templates/-t')

    def test_fail_if_no_input_directory(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'legacy-bake', '--output', 'out', '--image-name', 'image1', '--templates', 'templates'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --input/-i')

    def test_fail_if_no_image(self):
        with self.assertRaises(ValueError) as cm:
            self.under_test.parse_args(
                ['singularity', 'legacy-bake', '--input', 'dir1', '--output', 'out', '--templates', 'templates'])
        self.assertEqual(
            cm.exception.args[0], 'the following arguments are required: --image-name/-n')


def mock_function():
    pass


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
