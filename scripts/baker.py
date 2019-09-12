#!/usr/bin/env python3

import argparse
import sys
import os
import logging
from bakerlib.argument_parsing import new_argument_parser
from bakerlib.softwares import get_softwares
from bakerlib.main import decorate, preamble


##TODO Debug only if verbose, otherwise INFO
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s\t%(name)s\t{%(pathname)s:%(lineno)d}\t%(levelname)s\t%(message)s')
preamble()
parser = new_argument_parser(decorating=decorate)
arguments = parser.parse_args()
parameters = dict(vars(arguments))
if hasattr(arguments, "func"):
	del parameters["func"]
	arguments.func(**parameters)
else:
	parser.print_help()