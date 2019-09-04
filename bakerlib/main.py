import logging
import re

from bakerlib.softwares import get_softwares
from bakerlib.templating import TemplateRenderer

_logger = logging.getLogger('main')

def bake(input_dirs, output_dir, template_dir):
    _bake(input_dirs, output_dir, TemplateRenderer.new_instance(template_dir), get_softwares)

def _bake(input_dirs, output_dir, renderer, retrieve_software):
    softwares = retrieve_software(input_dirs)
    _logger.debug("Software retrieved: %s", softwares)
    for software in softwares:
        _logger.info("Processing %s version %s", software["name"], software["version"])
        wrapper_dir = "%s/%s/wrappers" % (output_dir, software["name"])
        for function in software['functions']:
            data = function.split("=")
            (script_name, executable) = (data[0], data[1]) if len(
                data) == 2 else (data[0], data[0])
            renderer.create_script(
                wrapper_dir, script_name, software, executable)