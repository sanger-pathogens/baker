import argparse

def new_argument_parser(factory=lambda name:argparse.ArgumentParser(prog=name)):
    parser = factory('baker')
    subparsers = parser.add_subparsers(help='sub-command help')
    bake_parser = subparsers.add_parser('bake', help='Generate wrappers for all softwares')
    bake_parser.add_argument('directories', metavar='directory', nargs='+', help='directory of yaml file to process')
    bake_parser.add_argument('-output', required=True, help='output directory for configurations and wrappers')
    return parser
