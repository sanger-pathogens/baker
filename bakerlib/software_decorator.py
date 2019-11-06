import logging

_logger = logging.getLogger('decorator')


class SoftwareDecorator:

    def __init__(self, output_format, renderer, software_repository):
        self.output_format = output_format
        self.renderer = renderer
        self.software_repository = software_repository

    def decorate(self):
        for software in self.software_repository.get_software_catalog():
            _logger.debug("Processing %s version %s", software["name"], software["version"])
            to_render = dict(software)
            filename = self.output_format.format_map(to_render)
            self.renderer.create_file(filename, to_render)

    def __call__(self):
        self.decorate()
