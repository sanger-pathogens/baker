#!/usr/bin/env python3

import argparse
import sys
import os
import pkg_resources
from jinja2 import Environment, PackageLoader
from bakerlib.argument_parsing import new_argument_parser
from bakerlib.softwares import get_softwares
from bakerlib.main import bake


# version = ''
# try:
# 	version = pkg_resources.get_distribution("MYPROJECT").version
# except pkg_resources.DistributionNotFound:
# 	version = 'x.y.z'

parser = new_argument_parser(baking=bake)
arguments = parser.parse_args()
if hasattr(arguments, "func"):
	parameters = dict(vars(arguments))
	del parameters["func"]
	arguments.func(**parameters)
else:
	parser.print_help()