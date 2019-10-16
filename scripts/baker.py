#!/usr/bin/env python3

import argparse
import sys
import os
import logging
from bakerlib.argument_parsing import ArgumentParserBuilder
from bakerlib.softwares import get_softwares
from bakerlib.main import decorate, get_version, singularity_check, singularity_bake


parser = ArgumentParserBuilder.new_instance()\
    .with_decorating(decorate)\
    .with_version(get_version)\
    .with_singularity_check(singularity_check)\
    .with_singularity_bake(singularity_bake)\
    .with_verbose()\
    .build()
arguments = parser.parse_args()
parameters = dict(vars(arguments))
level=logging.DEBUG
if hasattr(arguments, "verbose"):
    del parameters["verbose"]
    level=logging.DEBUG if arguments.verbose else logging.INFO

logging.basicConfig(level=level,
                    format='%(asctime)s\t%(name)s\t{%(pathname)s:%(lineno)d}\t%(levelname)s\t%(message)s')

if hasattr(arguments, "func"):
    del parameters["func"]
    arguments.func(**parameters)
else:
    parser.print_help()
