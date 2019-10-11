import logging
import re

from pkg_resources import get_distribution, DistributionNotFound
from bakerlib.softwares import get_softwares
from bakerlib.templating import TemplateRenderer

_logger = logging.getLogger('main')


def get_version():
    try:
        return get_distribution("baker").version
    except DistributionNotFound:
        return '<Unknown>'

def decorate(input_dir, output_dir, template_dir):
    _decorate(input_dir, output_dir, TemplateRenderer.new_instance(
        template_dir), get_softwares)

def singularity_check(input_dir, output_dir):
    print("Checking %s reconciles with %s" % (input_dir, output_dir))

def _decorate(input_dir, output_dir, renderer, retrieve_software):
    softwares = retrieve_software([input_dir])
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
