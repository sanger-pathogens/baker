import os
import yaml
import glob
import logging

_logger = logging.getLogger('softwares')

def get_softwares(inputs):
    filenames = _list_yaml_files(inputs)
    _logger.debug("Yaml files discovered: %s", filenames)
    softwares = []
    for filename in filenames:
        software = _read_software_from_file(filename)
        if software is not None:
            softwares.append(software)
    return softwares

def _read_software(infile):
    try:
        return yaml.load(infile, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        _logger.exception("Could not load yaml")
        return None

def _read_software_from_file(filename):
    _logger.info("Loading software from file %s", filename)
    with open(filename, 'r') as input:
        return _read_software(input)

def _list_yaml_files(inputs):
    files = []
    for input in inputs:
        files.extend(glob.glob("%s/*.yml" % input))
        files.extend(glob.glob("%s/*.yaml" % input))
    return files
    