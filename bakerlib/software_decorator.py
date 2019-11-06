import logging

_logger = logging.getLogger('decorator')


class SoftwareDecorator:

    def __init__(self, output_dir, renderer, software_repository):
        self.output_dir = output_dir
        self.renderer = renderer
        self.software_repository = software_repository

    def decorate(self):
        for software in self.software_repository.get_software_catalog():
            _logger.debug("Processing %s version %s", software["name"], software["version"])
            software_directory = software["name"]
            wrapper_directory = "%s/%s" % (self.output_dir, software_directory)
            to_render = dict(software)
            self.renderer.create_file(wrapper_directory, software["version"], to_render)

    def __call__(self):
        self.decorate()
