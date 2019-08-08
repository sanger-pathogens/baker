import argparse


def new_argument_parser(baking, factory=lambda: argparse.ArgumentParser()):
    parser = factory()
    subparsers = parser.add_subparsers(help='sub-command help')
    bake_parser = subparsers.add_parser(
        'bake', help='Generate wrappers for all softwares')
    bake_parser.add_argument('directories', metavar='directory',
                             nargs='+', help='directory of yaml file to process')
    bake_parser.add_argument(
        '--output','-o', required=True, help='output directory for configurations and wrappers')
    bake_parser.set_defaults(func=baking)
    return parser
