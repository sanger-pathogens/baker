
from bakerlib.softwares import get_softwares
import logging

_logger = logging.getLogger('main')

def bake(input_dirs, output_dir):
	_logger.debug("Baking input: %s, output: %s", input_dirs, output_dir)
	softwares = get_softwares(input_dirs)
	_logger.debug("Software loaded: %s", softwares)
	return softwares
