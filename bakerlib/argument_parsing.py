import argparse


def new_argument_parser(decorating, baking, factory=lambda: argparse.ArgumentParser()):
    parser = factory()
    subparsers = parser.add_subparsers(help='sub-command help')
    _build_decorate_parser(subparsers, decorating)
    _build_bake_parser(subparsers, baking)
    return parser

def _build_decorate_parser(subparsers, decorating):
    decorate_parser = subparsers.add_parser(
        'decorate', help='Generate wrappers for all softwares')
    decorate_parser.add_argument('input_dirs', metavar='directory',
                             nargs='+', help='directory of yaml file to process')
    decorate_parser.add_argument(
        '--output','-o', dest='output_dir', required=True, help='output directory for configurations and wrappers')
    decorate_parser.add_argument(
        '--templates','-t', dest='template_dir', required=True, help='directory containing the jinja2 templates')
    decorate_parser.set_defaults(func=decorating)

def _build_bake_parser(subparsers, decorating):
    bake_parser = subparsers.add_parser(
        'bake', help='Generate singularity images')
    bake_parser.add_argument('input_dirs', metavar='directory',
                             nargs='+', help='directory of yaml file to process')
    bake_parser.add_argument(
        '--output','-o', dest='output_dir', required=True, help='output directory for configurations and wrappers')
    bake_parser.add_argument(
        '--image','-i', dest='image', required=False, default=None , help='the image to build')
    bake_parser.add_argument(
        '--config','-c', dest='config', required=False, default=None , help='the docker registry access config')
    bake_parser.add_argument(
        '--templates','-t', dest='template_dir', required=True, help='directory containing the jinja2 templates')
    bake_parser.set_defaults(func=decorating)
