import logging

_logger = logging.getLogger('decorator')


class FunctionDecorator:

    def __init__(self, output_dir, renderer, software_repository):
        self.output_dir = output_dir
        self.renderer = renderer
        self.software_repository = software_repository

    def decorate(self):
        for software in self.software_repository.get_software_catalog():
            _logger.debug("Processing %s version %s", software["name"], software["version"])
            software_directory = "%s/%s" % (software["name"], software["version"])
            relative_wrapper_directory = "%s/wrappers" % software_directory
            wrapper_directory = "%s/%s" % (self.output_dir, relative_wrapper_directory)
            for function in software['exported_functions']:
                to_render = dict(software)
                to_render["function"] = function
                self.renderer.create_file(wrapper_directory, function["script_name"], to_render)

    def __call__(self):
        self.decorate()
