import unittest
from os.path import dirname, abspath

from jinja2 import Environment, FileSystemLoader

from bakerlib.templating import ScriptTemplateRenderer

DEFAULT_TEMPLATE = "default.template"
DEFAULT_FILE_MODE = 0
A_FUNCTION_TO_RENDER = {
    "url": "docker://some_url",
    "function": {"script_name": "script_name", "executable": "executable", "args": []}}

A_TEMPLATE = "A_TEMPLATE"


class TestScriptTemplateRenderer(unittest.TestCase):

    def setUp(self):
        loader = FileSystemLoader(dirname(abspath(__file__)))
        self.under_test = ScriptTemplateRenderer(Environment(loader=loader), DEFAULT_TEMPLATE, DEFAULT_FILE_MODE)

    def test_should_render_default_template_software(self):
        actual = self.under_test.render(A_FUNCTION_TO_RENDER)
        self.assertEqual(actual, "default\ndocker://some_url\nexecutable")
