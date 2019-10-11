#!/usr/bin/env python3

import argparse
import sys
import os
import logging
from bakerlib.argument_parsing import ArgumentParserBuilder
from bakerlib.softwares import get_softwares
from bakerlib.main import decorate, get_version, singularity_check


# TODO Debug only if verbose, otherwise INFO
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s\t%(name)s\t{%(pathname)s:%(lineno)d}\t%(levelname)s\t%(message)s')
parser = ArgumentParserBuilder.new_instance()\
    .with_decorating(decorate)\
    .with_version(get_version)\
    .with_singularity_check(singularity_check)\
    .build()
arguments = parser.parse_args()
parameters = dict(vars(arguments))
if hasattr(arguments, "func"):
    del parameters["func"]
    arguments.func(**parameters)
else:
    parser.print_help()
