import unittest
from os.path import dirname, abspath

from jinja2 import Environment, FileSystemLoader

from bakerlib.templating import ScriptTemplateRenderer

DEFAULT_TEMPLATE = "default.template"
A_FUNCTION_TO_RENDER = {
    "url": "docker://someurl",
    "function": {"script_name": "script_name", "executable": "executable", "args": []}}

A_TEMPLATE = "A_TEMPLATE"


class TestScriptTemplateRenderer(unittest.TestCase):

    def setUp(self):
        self.under_test = ScriptTemplateRenderer(Environment(loader=FileSystemLoader(dirname(abspath(__file__)))))

    def test_should_render_default_template_software(self):
        actual = self.under_test.render(DEFAULT_TEMPLATE, A_FUNCTION_TO_RENDER)
        self.assertEqual(actual, "default\ndocker://someurl\nexecutable")
