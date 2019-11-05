#!/usr/bin/env python3

import logging
import sys

from bakerlib.dependency_injection import BakerDI

LOG_FORMAT = '%(asctime)s\t%(name)s\t{%(pathname)s:%(lineno)d}\t%(levelname)s\t%(message)s'


def reconfigure_logs(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format=LOG_FORMAT)


def main():
    log = None
    try:
        container = BakerDI()
        reconfigure_logs(container.verbose)
        log = logging.getLogger('main')
        command = container.command
        command()
        return 0
    except Exception as err:
        if log is not None:
            log.exception('Unexpected error caught:')
        else:
            sys.stderr.write('ERROR: %sn' % str(err))
        return 1


def basic_logs():
    logging.basicConfig(level=logging.CRITICAL, format=LOG_FORMAT)


if __name__ == '__main__':
    sys.exit(main())
