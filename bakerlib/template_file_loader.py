from os import path

from jinja2 import BaseLoader, TemplateNotFound
from jinja2.utils import open_if_exists


class TemplateFileLoader(BaseLoader):
    """Loads templates from the file system.  This loader assume the template name is the file to load
    (ie /path/to/template/template)
    """

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def get_source(self, environment, template):
        f = open_if_exists(template)
        if f is None:
            raise TemplateNotFound(template)
        try:
            contents = f.read().decode(self.encoding)
        finally:
            f.close()

        modification_time = path.getmtime(template)

        def up_to_date():
            try:
                return path.getmtime(template) == modification_time
            except OSError:
                return False

        return contents, template, up_to_date

    def list_templates(self):
        return set()
