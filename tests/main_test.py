import unittest
import os
import argparse
import scripts

from unittest.mock import MagicMock, call
from bakerlib.main import _decorate, _singularity_check
from bakerlib.main import _decorate, _singularity_check
from os.path import dirname, abspath

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
ANOTHER_SOFTWARE_FUNCTION = {
    "script_name": "interesting", "executable": "facts", "args": []}
ANOTHER_SOFTWARE = {
    "url": "docker://someurl/gff3toembl:1.1.4",
    "name": "gff3toembl",
    "version": "1.1.4",
    "exported_functions": [ANOTHER_SOFTWARE_FUNCTION],
    "image": ANOTHER_IMAGE
}

AN_OUTPUT_DIR = "AN_OUTPUT_DIR"
A_TEMPLATE_DIR = "A_TEMPLATE_DIR"


class TestBaker(unittest.TestCase):

    def test_should_decorate_softwares(self):
        mock_renderer = MagicMock()
        _decorate(output_dir=AN_OUTPUT_DIR, renderer=mock_renderer,
                  retrieve_software=lambda: [A_SOFTWARE, ANOTHER_SOFTWARE])
        self.assertCountEqual(mock_renderer.create_script.call_args_list,
                              [
                                  call('AN_OUTPUT_DIR/artemis/18.0.3/wrappers',
                                       'art', A_SOFTWARE, A_SOFTWARE_FUNCTIONS_1),
                                  call('AN_OUTPUT_DIR/artemis/18.0.3/wrappers',
                                       'act', A_SOFTWARE, A_SOFTWARE_FUNCTIONS_2),
                                  call('AN_OUTPUT_DIR/gff3toembl/1.1.4/wrappers', 'interesting', ANOTHER_SOFTWARE, ANOTHER_SOFTWARE_FUNCTION)])

class TestSingularityChecker(unittest.TestCase):
    def test_check_singularity_images(self):
        mock_image_repo = MagicMock()
        mock_image_repo.get_images.return_value = [AN_IMAGE, ANOTHER_IMAGE]
        mock_checker = MagicMock()
        _singularity_check(image_repo=mock_image_repo, retrieve_softwares=lambda: [
                           A_SOFTWARE, ANOTHER_SOFTWARE], checker=mock_checker)
        self.assertEqual(mock_checker.check.call_args_list, [call([
                           A_SOFTWARE, ANOTHER_SOFTWARE], [AN_IMAGE, ANOTHER_IMAGE])])

