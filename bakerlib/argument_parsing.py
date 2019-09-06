import argparse


def new_argument_parser(decorating, factory=lambda: argparse.ArgumentParser()):
    parser = factory()
    subparsers = parser.add_subparsers(help='sub-command help')
    bake_parser = subparsers.add_parser(
        'decorate', help='Generate wrappers for all softwares')
    bake_parser.add_argument('input_dirs', metavar='directory',
                             nargs='+', help='directory of yaml file to process')
    bake_parser.add_argument(
        '--output','-o', dest='output_dir', required=True, help='output directory for configurations and wrappers')
    bake_parser.add_argument(
        '--templates','-t', dest='template_dir', required=True, help='directory containing the jinja2 templates')
    bake_parser.set_defaults(func=decorating)
    return parser
