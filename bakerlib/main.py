import logging
import re

from pkg_resources import get_distribution, DistributionNotFound
from bakerlib.softwares import get_softwares
from bakerlib.templating import TemplateRenderer

_logger = logging.getLogger('main')


def _get_version():
    try:
        return get_distribution("baker").version
    except DistributionNotFound:
        return '<Unknown>'

def preamble():
    _logger.info("Baker version %s", _get_version())


def decorate(input_dirs, output_dir, template_dir):
    _decorate(input_dirs, output_dir, TemplateRenderer.new_instance(
        template_dir), get_softwares)


def _decorate(input_dirs, output_dir, renderer, retrieve_software):
    softwares = retrieve_software(input_dirs)
    _logger.debug("Software retrieved: %s", softwares)
    for software in softwares:
        _logger.info("Processing %s version %s",
                     software["name"], software["version"])
        software_directory = "%s/%s" % (software["name"], software["version"])
        wrapper_directory = "%s/wrappers" % software_directory
        output_wrapper_directory = "%s/%s" % (output_dir, wrapper_directory)
        for function in software['exported_functions']:
            renderer.create_script(
                output_wrapper_directory, function["script_name"], software, function)
