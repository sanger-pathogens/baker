import logging
import re

from pkg_resources import get_distribution, DistributionNotFound
from bakerlib.softwares import get_softwares
from bakerlib.templating import TemplateRenderer
from bakerlib.images import ImageRepository
from bakerlib.singularity import SingularityChecker

_logger = logging.getLogger('main')


def get_version():
    try:
        return get_distribution("baker").version
    except DistributionNotFound:
        return '<Unknown>'

def decorate(input_dir, output_dir, template_dir):
    _decorate(output_dir, TemplateRenderer.new_instance(
        template_dir), lambda : get_softwares([input_dir]))

def singularity_check(input_dir, output_dir):
    _logger.debug("Checking %s reconciles with %s" % (input_dir, output_dir))
    image_repo = ImageRepository(output_dir)
    checker = SingularityChecker(lambda s: print("missing %s" % s), lambda s: print("unknown %s" % s))
    _singularity_check(lambda : get_softwares([input_dir]), image_repo, checker)

def singularity_build(input_dir, output_dir, missing, images):
    _logger.debug("Building missing images between %s and %s" % (input_dir, output_dir))
    image_repo = ImageRepository(output_dir)
    checker = SingularityChecker(lambda s: print("building image %s" % s), lambda s: None)
    _singularity_check(lambda : get_softwares([input_dir]), image_repo, checker)

def _singularity_check(retrieve_softwares, image_repo, checker):
    softwares = retrieve_softwares()
    images = image_repo.get_images()
    checker.check(softwares, images)
    
def _decorate(output_dir, renderer, retrieve_software):
    softwares = retrieve_software()
    for software in softwares:
        _logger.debug("Processing %s version %s",
                     software["name"], software["version"])
        software_directory = "%s/%s" % (software["name"], software["version"])
        wrapper_directory = "%s/wrappers" % software_directory
        output_wrapper_directory = "%s/%s" % (output_dir, wrapper_directory)
        for function in software['exported_functions']:
            renderer.create_script(
                output_wrapper_directory, function["script_name"], software, function)
