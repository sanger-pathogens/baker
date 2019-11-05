import logging
from os import makedirs, chmod

_logger = logging.getLogger('templating')


class ScriptTemplateRenderer:

    def __init__(self, environment):
        self.jinja2_environment = environment

    def render(self, template, parameters):
        renderer = self.jinja2_environment.get_template(template)
        return renderer.render(**parameters)

    def create_file(self, directory, name, parameters, template, file_mode):
        content = self.render(template, parameters)
        makedirs(directory, exist_ok=True)
        filename = "%s/%s" % (directory, name)
        with open(filename, 'w') as bash_wrapper:
            print(content, file=bash_wrapper)
        chmod(filename, file_mode)
        _logger.debug("Created file %s", name)
