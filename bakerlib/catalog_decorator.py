import logging

_logger = logging.getLogger('decorator')


class CatalogDecorator:

    def __init__(self, output_format, renderer, software_repository):
        self.output_format = output_format
        self.renderer = renderer
        self.software_repository = software_repository

    def decorate(self):
        _logger.debug("Processing software catalog")
        to_render = {"softwares": self.software_repository.get_software_catalog()}
        filename = self.output_format.format_map(to_render)
        self.renderer.create_file(filename, to_render)

    def __call__(self):
        self.decorate()
