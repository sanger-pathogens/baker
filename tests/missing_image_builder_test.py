import unittest
from unittest.mock import MagicMock, call

from bakerlib.missing_image_builder import MissingImageBuilder

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

AN_OUTPUT_DIR = "AN_OUTPUT_DIR"
A_TEMPLATE_DIR = "A_TEMPLATE_DIR"

A_FILE_MODE = 0o555



class TestMissingImageBuilder(unittest.TestCase):

    def setUp(self):
        self.mock_image_repo = MagicMock()
        self.mock_image_repo.get_images.return_value = [AN_IMAGE, ANOTHER_IMAGE]
        self.mock_checker = MagicMock()
        self.under_test = MissingImageBuilder(image_repo=self.mock_image_repo, software_catalog=[
            A_SOFTWARE, ANOTHER_SOFTWARE], checker=self.mock_checker)

    def test_check_singularity_images(self):
        self.under_test.check()
        self.assertEqual(self.mock_checker.check.call_args_list, [call([
            A_SOFTWARE, ANOTHER_SOFTWARE], [AN_IMAGE, ANOTHER_IMAGE])])
