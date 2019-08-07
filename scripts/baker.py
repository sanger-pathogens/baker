#!/usr/bin/env python3

import argparse
import sys
import os
import pkg_resources

from bakerlib.MYCLASS import MYCLASS
from bakerlib.InputTypes import InputTypes

version = ''
try:
	version = pkg_resources.get_distribution("MYPROJECT").version
except pkg_resources.DistributionNotFound:
	version = 'x.y.z'

parser = argparse.ArgumentParser(
	description = 'what Tim did next',
	usage = 'MYSCRIPT [options]', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--foo', help='Example option foo', type=InputTypes.is_foo_valid )
parser.add_argument('--output_file', '-o', help='Output file [STDOUT]')
parser.add_argument('--verbose', '-v', action='store_true', help='Turn on debugging [%(default)s]', default = False)
parser.add_argument('--version', action='version', version=str(version))

options = parser.parse_args()

thingy = MYCLASS(options)
thingy.run()
