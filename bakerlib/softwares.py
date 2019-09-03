import os
import yaml
import glob

def get_softwares(inputs):
    filenames = _list_yaml_files(inputs)
    softwares = []
    for filename in filenames:
        software = _read_software_from_file(filename)
        if software is not None:
            softwares.append(software)
    return softwares

def _read_software(infile):
    try:
        return yaml.load(infile, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        print(exc)
        return None

def _read_software_from_file(filename):
    with open(filename, 'r') as input:
        return _read_software(input)

def _list_yaml_files(inputs):
    files = []
    for input in inputs:
        files.extend(glob.glob("%s/*.yml" % input))
        files.extend(glob.glob("%s/*.yaml" % input))
    return files
    