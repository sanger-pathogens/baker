import argparse

class ArgumentParserBuilder:

    @staticmethod
    def new_instance(factory=lambda: argparse.ArgumentParser()):
        return ArgumentParserBuilder(factory())
        
    def __init__(self, parser):
        self.parser = parser
        self.subparsers = self.parser.add_subparsers(help='sub-command help')

    def with_version(self, version):
        self.parser.add_argument('--version', action='version', version=version)
        return self

    def with_decorating(self, decorating):
        decorate_parser = self.subparsers.add_parser(
            'decorate', help='Generate wrappers for all softwares')
        decorate_parser.add_argument(
            '--input','-i', dest='input_dir', required=True, help='directory of yaml file to process')
        decorate_parser.add_argument(
            '--output','-o', dest='output_dir', required=True, help='output directory for configurations and wrappers')
        decorate_parser.add_argument(
            '--templates','-t', dest='template_dir', required=True, help='directory containing the jinja2 templates')
        decorate_parser.set_defaults(func=decorating)
        return self

    def build(self):
        return self.parser
