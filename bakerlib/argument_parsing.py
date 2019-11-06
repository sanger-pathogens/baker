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

    def with_function_decorating(self, decorating):
        decorate_parser = self.decorate_sub_parsers.add_parser(
            'function', help='Decorate each function of each software')
        self._add_decoration_arguments(decorate_parser, decorating)
        return self

    def with_software_decorating(self, decorating):
        decorate_parser = self.decorate_sub_parsers.add_parser(
            'software', help='Decorate each software')
        self._add_decoration_arguments(decorate_parser, decorating)
        return self

    @staticmethod
    def _add_decoration_arguments(decorate_parser, decorating):
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
        decorate_parser.set_defaults(func=decorating)

    def with_singularity_check(self, reconciling):
        reconcile_parser = self.singularity_sub_parsers.add_parser(
            'check', help='Reconcile singularity images againts the software lists')
        reconcile_parser.add_argument(
            '--input', '-i', dest='input_dir', required=True,
            help='directory of software definition yaml files to process')
        reconcile_parser.add_argument(
            '--output', '-o', dest='output_dir', required=True, help='output directory for images')
        reconcile_parser.set_defaults(func=reconciling)
        return self

    def with_singularity_bake(self, baking):
        bake_parser = self.singularity_sub_parsers.add_parser(
            'bake', help='Build singularity images')
        bake_parser.add_argument(
            '--input', '-i', dest='input_dir', required=True,
            help='directory of software definition yaml files to process')
        bake_parser.add_argument(
            '--output', '-o', dest='output_dir', required=True, help='output directory for images')
        bake_parser.add_argument(
            '--config', '-c', dest='config', required=True, help='docker registry access config')
        group = bake_parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--missing', '-m', dest='missing', default=False, action='store_true', help='build all missing images')
        group.add_argument(
            '--image-name', '-n', dest='images', default=[], action='append', help='Specific image to build')
        bake_parser.set_defaults(func=baking)
        return self

    def with_legacy_bake(self, legacy_baking):
        bake_parser = self.singularity_sub_parsers.add_parser(
            'legacy-bake',
            help='Build singularity images using singularity recipes and templates.  This is legacy, prefer the use of docker images')
        bake_parser.add_argument(
            '--input', '-i', dest='input_dir', required=True,
            help='directory of software definition yaml files to process')
        bake_parser.add_argument(
            '--output', '-o', dest='output_dir', required=True, help='output directory for images')
        bake_parser.add_argument(
            '--templates', '-t', dest='template_dir', required=True, help='directory containing the jinja2 templates')
        bake_parser.add_argument(
            '--image-name', '-n', dest='images', required=True, action='append', help='Specific image to build')
        bake_parser.set_defaults(func=legacy_baking)
        return self

    def build(self):
        return self.parser
