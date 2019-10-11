import argparse


def new_argument_parser(decorating, version, factory=lambda: argparse.ArgumentParser()):
    parser = factory()
    
    parser.add_argument('--version', action='version', version=version)

    subparsers = parser.add_subparsers(help='sub-command help')
    bake_parser = subparsers.add_parser(
        'decorate', help='Generate wrappers for all softwares')
    bake_parser.add_argument(
        '--input','-i', dest='input_dir', required=True, help='directory of yaml file to process')
    bake_parser.add_argument(
        '--output','-o', dest='output_dir', required=True, help='output directory for configurations and wrappers')
    bake_parser.add_argument(
        '--templates','-t', dest='template_dir', required=True, help='directory containing the jinja2 templates')
    bake_parser.set_defaults(func=decorating)


    return parser
