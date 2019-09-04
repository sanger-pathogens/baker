import os
import yaml
import glob
import logging
import re

_logger = logging.getLogger('softwares')


class InvalidSoftwareError(Exception):
    pass


def _software_name_version_validation(software):
    if "name" not in software:
        raise InvalidSoftwareError("Name not in software " + software)
    if "version" not in software:
        raise InvalidSoftwareError("Version not in software " + software)

def _function_enrichments(software):
    exported_functions = []
    for function in software["functions"]:
        if isinstance(function, dict):
            if "args" not in function:
                function["args"] = []
            if "executable" not in function:
                function["executable"] = function["script_name"]
            exported_functions.append(function)
        elif isinstance(function, str):
            exported_functions.append({"script_name": function, "executable": function, "args": []})
    software["exported_functions"] = exported_functions

def _image_enrichment(software):
    if "image" not in software:
        software["image"] = software['name'] + \
            '-' + software['version'] + '.simg'


def _url_enrichments(software):
    if "url" in software:
        pattern = re.compile("^docker://.+/(?P<name>[^:]+):(?P<version>[^:]+)")
        match = pattern.search(software["url"])
        if match is not None:
            if "name" not in software:
                software["name"] = match.group("name")
            if "version" not in software:
                software["version"] = match.group("version")


def get_softwares(inputs, enrichments=[_url_enrichments, _software_name_version_validation, _image_enrichment, _function_enrichments]):
    filenames = _list_yaml_files(inputs)
    _logger.debug("Yaml files discovered: %s", filenames)
    softwares = []
    for filename in filenames:
        software = _read_software_from_file(filename)
        if software is not None:
            _enrich_software(enrichments, software)
            softwares.append(software)
    return softwares


def _enrich_software(enrichments, software):
    for enrichment in enrichments:
        enrichment(software)


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
