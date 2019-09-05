import logging
import re

from bakerlib.softwares import get_softwares
from bakerlib.templating import TemplateRenderer

_logger = logging.getLogger('main')


def decorate(input_dirs, output_dir, template_dir):
    _decorate(input_dirs, output_dir, TemplateRenderer.new_instance(
        template_dir), get_softwares)


def _decorate(input_dirs, output_dir, renderer, retrieve_software):
    softwares = retrieve_software(input_dirs)
    _logger.debug("Software retrieved: %s", softwares)
    for software in softwares:
        _logger.info("Processing %s version %s",
                     software["name"], software["version"])
        wrapper_dir = "%s/%s/wrappers" % (output_dir, software["name"])
        for function in software['exported_functions']:
            renderer.create_script(
                wrapper_dir, function["script_name"], software, function)
