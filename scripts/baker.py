#!/usr/bin/env python3

import argparse
import sys
import os
import pkg_resources

from bakerlib.argument_parsing import new_argument_parser

def bake(arguments):
	output_dir = arguments.output
	input_dirs = arguments.directories
	print("I am baking", output_dir, input_dirs)

# version = ''
# try:
# 	version = pkg_resources.get_distribution("MYPROJECT").version
# except pkg_resources.DistributionNotFound:
# 	version = 'x.y.z'

parser = new_argument_parser(baking=bake)
arguments = parser.parse_args()
if hasattr(arguments, "func"):
	arguments.func(arguments)
else:
	parser.print_help()