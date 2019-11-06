import logging
from os import makedirs, chmod
from os.path import dirname
_logger = logging.getLogger('templating')


class ScriptTemplateRenderer:

    def __init__(self, environment, template, file_mode):
        self.jinja2_environment = environment
        self.template = template
        self.file_mode = file_mode

    def render(self, parameters):
        renderer = self.jinja2_environment.get_template(self.template)
        return renderer.render(**parameters)

    def create_file(self, name, parameters):
        directory = dirname(name)
        content = self.render(parameters)
        makedirs(directory, exist_ok=True)
        with open(name, 'w') as bash_wrapper:
            print(content, file=bash_wrapper)
        chmod(name, self.file_mode)
        _logger.debug("Created file %s", name)
