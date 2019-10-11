import unittest
import scripts

from unittest.mock import MagicMock, call
from bakerlib.singularity import SingularityChecker

AN_IMAGE = "AN_IMAGE"
ANOTHER_IMAGE = "ANOTHER_IMAGE"

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
ANOTHER_SOFTWARE_FUNCTION = {
    "script_name": "interesting", "executable": "facts", "args": []}
ANOTHER_SOFTWARE = {
    "url": "docker://someurl/gff3toembl:1.1.4",
    "name": "gff3toembl",
    "version": "1.1.4",
    "exported_functions": [ANOTHER_SOFTWARE_FUNCTION],
    "image": ANOTHER_IMAGE
}


class TestSingularityChecker(unittest.TestCase):

    def setUp(self):
        self.mock_missing_images = MagicMock()
        self.mock_unknown_images = MagicMock()
        self.under_test = SingularityChecker(
            self.mock_missing_images, self.mock_unknown_images)

    def test_check_singularity_images(self):
        self.under_test.check([A_SOFTWARE, ANOTHER_SOFTWARE], [
                              AN_IMAGE, ANOTHER_IMAGE])
        self.assertEqual(self.mock_missing_images.call_count, 0)
        self.assertEqual(self.mock_unknown_images.call_count, 0)

    def test_check_singularity_images_unknown_images(self):
        self.under_test.check([A_SOFTWARE], [AN_IMAGE, ANOTHER_IMAGE])
        self.assertEqual(self.mock_missing_images.call_count, 0)
        self.assertCountEqual(self.mock_unknown_images.call_args_list, [
                              call(ANOTHER_IMAGE)])

    def test_check_singularity_images_missing_images(self):
        self.under_test.check([A_SOFTWARE, ANOTHER_SOFTWARE], [AN_IMAGE])
        self.assertCountEqual(self.mock_missing_images.call_args_list, [
                              call(ANOTHER_IMAGE)])
        self.assertEqual(self.mock_unknown_images.call_count, 0)
