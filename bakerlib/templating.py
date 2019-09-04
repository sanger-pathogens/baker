
import logging
from os import makedirs
from subprocess import run
from jinja2 import Environment, FileSystemLoader

_logger = logging.getLogger('templating')



class TemplateRenderer:
    @staticmethod
    def new_instance(directory):
        # TODO DI
        return TemplateRenderer(environment = Environment(loader=FileSystemLoader(directory)))

    def __init__(self, environment):
        self.jinja2_environment = environment

    def render(self, software, function):
        parameters = dict(software)
        parameters['function'] = function
        template = self.__select_template(software)
        return template.render(**parameters)

    def create_script(self, directory, name, software, function):
        content = self.render(software, function)
        makedirs(directory, exist_ok=True)
        script_name = "%s/%s" % (directory, name)
        with open(script_name, 'w') as bash_wrapper:
            print(content, file=bash_wrapper)
        run(["chmod", "-R", "555", script_name])
        _logger.debug("Created script %s", name)

    def __select_template_name(self, software):
        return software["function_template"] if "function_template" in software else "default.template"

    def __select_template(self, software):
        template = self.__select_template_name(software)
        return self.jinja2_environment.get_template(template)



