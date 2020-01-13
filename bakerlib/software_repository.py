import glob
import logging

import yaml

_logger = logging.getLogger('softwares')


class InvalidSoftwareError(Exception):
    pass


class SoftwareRepository:
    def __init__(self, input_dir, enrichment_list):
        self.input_dir = input_dir
        self.enrichment_list = enrichment_list

    def get_software_catalog(self):
        files = self._list_yaml_files(self.input_dir)
        _logger.debug("Yaml files discovered: %s", files)
        software_catalog = []
        for file in files:
            software = self._read_software_from_file(file)
            if software is not None:
                self._enrich_software(software)
                software_catalog.append(software)
        _logger.debug("Software retrieved: %s", software_catalog)
        return software_catalog

    def _enrich_software(self, software):
        for enrich in self.enrichment_list:
            enrich(software)

    @staticmethod
    def _read_software(infile):
        return yaml.load(infile, Loader=yaml.SafeLoader)

    def _read_software_from_file(self, filename):
        _logger.debug("Loading software from file %s", filename)
        with open(filename, 'r') as file:
            return self._read_software(file)

    @staticmethod
    def _list_yaml_files(directory):
        files = []
        files.extend(glob.glob("%s/*.yml" % directory))
        files.extend(glob.glob("%s/*.yaml" % directory))
        return files
