import argparse


class ArgumentParserBuilder:

    @staticmethod
    def new_instance(factory=lambda: argparse.ArgumentParser()):
        return ArgumentParserBuilder(factory())

    def __init__(self, parser):
        self.parser = parser
        self.subparsers = self.parser.add_subparsers(help='sub-command help')
        singularity_parser = self.subparsers.add_parser(
            'singularity', help='Singularity image related actions')
        decorate_parser = self.subparsers.add_parser(
            'decorate', help='Decoration related actions')
        self.singularity_sub_parsers = singularity_parser.add_subparsers(help='singularity image sub-command help')
        self.decorate_sub_parsers = decorate_parser.add_subparsers(help='decoration sub-command help')

    def with_version(self, version):
        self.parser.add_argument(
            '--version', action='version', version=version)
        return self

    def with_verbose(self):
        self.parser.add_argument(
            '--verbose', '-v', dest='verbose', default=False, action='store_true')
        return self

    def with_decorating(self, target, decorating):
        decorate_parser = self.decorate_sub_parsers.add_parser(
            target, help='Decorate ' + target)
        decorate_parser.add_argument('--input', '-i', dest='input_dir', required=True,
                                     help='directory of software catalog (yaml files to process)')
        decorate_parser.add_argument('--output', '-o', dest='output_format', required=True,
                                     help='output format used for generated files, ie /some/path/{name}/{version}.txt'
                                          '.  Function atributes need double curly brackets: {{script_name}}')
        decorate_parser.add_argument(
            '--template', '-t', dest='template', required=True, help='the jinja2 template to use to decorate')
        decorate_parser.add_argument(
            '--file-mode', '-f', dest='file_mode', required=True, type=lambda x: int(x, 0),
            help='the mode/permission of the generated output files, ie 0o555')
        decorate_parser.add_argument('--images', '-m', dest='images', default=None, required=False,
                                     help='Directory of images already built')
        decorate_parser.set_defaults(func=decorating)
        return self

    def build(self):
        return self.parser
