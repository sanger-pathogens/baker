import unittest

from os.path import dirname, abspath
from unittest.mock import MagicMock
from bakerlib.templating import TemplateRenderer

DEFAULT_TEMPLATE = "default.template"
CUSTOM_TEMPLATE = "generic_template.template"
A_CUSTOM_TEMPLATE_BASED_SOFTWARE = {"name": "artemis",
                                    "version": "18.0.3",
                                    "function_template": CUSTOM_TEMPLATE,
                                    "docker_image": "sangerpathogens/artemis:release-v18.0.3"
                                    }
A_DEFAULT_TEMPLATE_BASED_SOFTWARE = {
    "url": "docker://someurl"}


class TestTemplateSelector(unittest.TestCase):
    def setUp(self):
        self.under_test = TemplateRenderer.new_instance(
            dirname(abspath(__file__)))

    def test_should_render_custom_template_software(self):
        actual = self.under_test.render(
            A_CUSTOM_TEMPLATE_BASED_SOFTWARE, "executable")
        self.assertEqual(
            actual, "generic_template\nartemis\n18.0.3\nexecutable")

    def test_should_render_default_template_software(self):
        actual = self.under_test.render(
            A_DEFAULT_TEMPLATE_BASED_SOFTWARE, "executable")
        self.assertEqual(actual, "default\ndocker://someurl\nexecutable")
