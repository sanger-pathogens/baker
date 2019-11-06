import logging
from os import makedirs, chmod

_logger = logging.getLogger('templating')


class ScriptTemplateRenderer:

    def __init__(self, environment, template, file_mode):
        self.jinja2_environment = environment
        self.template = template
        self.file_mode = file_mode

    def render(self, parameters):
        renderer = self.jinja2_environment.get_template(self.template)
        return renderer.render(**parameters)

    def create_file(self, directory, name, parameters):
        content = self.render(parameters)
        makedirs(directory, exist_ok=True)
        filename = "%s/%s" % (directory, name)
        with open(filename, 'w') as bash_wrapper:
            print(content, file=bash_wrapper)
        chmod(filename, self.file_mode)
        _logger.debug("Created file %s", name)
