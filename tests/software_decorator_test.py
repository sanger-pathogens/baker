import unittest
from unittest.mock import MagicMock, call

from bakerlib.software_decorator import SoftwareDecorator

AN_IMAGE = "AN_IMAGE"
ANOTHER_IMAGE = "ANOTHER_IMAGE"

AN_INPUT_DIR = 'AN INPUT DIRECTORY'
A_SOFTWARE_FUNCTIONS_1 = {"script_name": "art",
                          "executable": "art", "args": []}
A_SOFTWARE_FUNCTIONS_2 = {"script_name": "act",
                          "executable": "act", "args": []}
A_SOFTWARE = {
    "name": "artemis",
    "version": "18.0.3",
    "docker_image": "sangerpathogens/artemis:release-v18.0.3",
    "exported_functions": [A_SOFTWARE_FUNCTIONS_1, A_SOFTWARE_FUNCTIONS_2],
    "image": AN_IMAGE
}

A_FUNCTION_TO_RENDER_1 = {
    "name": "artemis",
    "version": "18.0.3",
    "docker_image": "sangerpathogens/artemis:release-v18.0.3",
    "exported_functions": [A_SOFTWARE_FUNCTIONS_1, A_SOFTWARE_FUNCTIONS_2],
    "image": AN_IMAGE,
    "function": A_SOFTWARE_FUNCTIONS_1
}

A_FUNCTION_TO_RENDER_2 = {
    "name": "artemis",
    "version": "18.0.3",
    "docker_image": "sangerpathogens/artemis:release-v18.0.3",
    "exported_functions": [A_SOFTWARE_FUNCTIONS_1, A_SOFTWARE_FUNCTIONS_2],
    "image": AN_IMAGE,
    "function": A_SOFTWARE_FUNCTIONS_2
}

ANOTHER_SOFTWARE_FUNCTION = {
    "script_name": "interesting", "executable": "facts", "args": []}
ANOTHER_SOFTWARE = {
    "url": "docker://someurl/gff3toembl:1.1.4",
    "name": "gff3toembl",
    "version": "1.1.4",
    "exported_functions": [ANOTHER_SOFTWARE_FUNCTION],
    "image": ANOTHER_IMAGE
}

ANOTHER_FUNCTION_TO_RENDER = {
    "url": "docker://someurl/gff3toembl:1.1.4",
    "name": "gff3toembl",
    "version": "1.1.4",
    "exported_functions": [ANOTHER_SOFTWARE_FUNCTION],
    "image": ANOTHER_IMAGE,
    "function": ANOTHER_SOFTWARE_FUNCTION
}

AN_OUTPUT_DIR = "AN_OUTPUT_DIR/{name}/{version}"
A_TEMPLATE_DIR = "A_TEMPLATE_DIR"

A_FILE_MODE = 0o555


class TestDecorator(unittest.TestCase):

    def setUp(self):
        self.mock_renderer = MagicMock()
        self.mock_software_repository = MagicMock()
        self.mock_software_repository.get_software_catalog.return_value = [A_SOFTWARE, ANOTHER_SOFTWARE]
        self.under_test = SoftwareDecorator(output_format=AN_OUTPUT_DIR, renderer=self.mock_renderer,
                                            software_repository=self.mock_software_repository)

    def test_should_decorate_softwares(self):
        self.under_test.decorate()
        self.assertCountEqual(self.mock_renderer.create_file.call_args_list,
                              [
                                  call('AN_OUTPUT_DIR/artemis/18.0.3', A_SOFTWARE),
                                  call('AN_OUTPUT_DIR/gff3toembl/1.1.4', ANOTHER_SOFTWARE)])
