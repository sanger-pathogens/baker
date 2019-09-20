from logging import getLogger
from subprocess import Popen
from pkg_resources import get_distribution, DistributionNotFound
from bakerlib.softwares import get_softwares
from bakerlib.templating import TemplateRenderer
from jinja2 import Environment, FileSystemLoader
from os.path import isfile
import os
from re import compile
from yaml import load, SafeLoader, YAMLError
import yaml
_logger = getLogger('main')

def _read_config(config):
    try:
        with open(config, 'r') as input:
            return yaml.load(input, Loader=SafeLoader)
    except YAMLError:
        _logger.exception("Could not load yaml " +config)
        return None

def _find_extra(software, config):
    pattern = compile("^docker://(?P<server>[^/:]+).*$")
    match = pattern.search(software["url"])
    if match is not None:
        server = match.group("server")
        if server in config:
            l = config[server]
            return ';'.join(l) + ';'
    return ''

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


def bake(image, input_dirs, output_dir, template_dir, config):
    _bake(image, input_dirs, output_dir, template_dir, get_softwares, _read_config(config))


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


def _bake(image, input_dirs, output_dir, template_dir, retrieve_software, docker_config):
    softwares = retrieve_software(input_dirs)
    _logger.debug("Software retrieved: %s", softwares)
    missing = [s for s in softwares if _needs_building(s, image, output_dir)]
    for software in missing:
        _logger.info("Baking %s version %s",
                     software["name"], software["version"])
        _bake_software(software, input_dirs, output_dir, template_dir, docker_config)


def _needs_building(software, image, output_dir):
    return (image is None or software["image"] == image) and not isfile("%s/%s" % (output_dir, software["image"]))

def _shell(command):
    p = Popen(command, shell=True)
    p.wait()


def _bake_software(software, input_dirs, output_dir, template_dir, docker_config):
    output_image = "%s/%s" % (output_dir, software["image"])
    if 'url' in software:
        extra = _find_extra(software, docker_config)
        _shell("rm -f '%s'" % output_image)
        _shell("%ssingularity build '%s' '%s'" % (extra, output_image, software["url"]))
        _logger.debug("Built image: %s", output_image)
        return
    recipe = output_image + '.recipe'
    #_shell("rm -f %s" % recipe)
    env = Environment(
        loader=FileSystemLoader(template_dir)
    )
    with open(recipe, 'w') as recipe_file:
        template = env.get_template(software['template'])
        print(template.render(software), file=recipe_file)

    _shell("rm -f '%s'" % output_image)
    _shell("singularity build --fakeroot '%s' '%s'" % (output_image, recipe))
    #_shell("rm -f %s" % recipe)
    _logger.debug("Built image: %s", output_image)
