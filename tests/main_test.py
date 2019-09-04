import unittest
import os
import argparse
import scripts

from unittest.mock import MagicMock, call
from bakerlib.main import _bake
from os.path import dirname, abspath


AN_INPUT_DIR = 'AN INPUT DIRECTORY'
ANOTHER_INPUT_DIR = 'ANOTHER INPUT DIRECTORY'
A_SOFTWARE = {"name": "artemis",
                                    "version": "18.0.3",
                                    "docker_image": "sangerpathogens/artemis:release-v18.0.3",
                                    "functions": ["art", "act"]
                                    }
ANOTHER_SOFTWARE = {
    "url": "docker://someurl/gff3toembl:1.1.4", 
    "name": "gff3toembl",
    "version": "1.1.4",                                              
    "functions": ["interesting=facts"]
}
AN_OUTPUT_DIR = "AN_OUTPUT_DIR"
A_TEMPLATE_DIR = "A_TEMPLATE_DIR"





def mock_retrieve_software(value):
    result = []
    if AN_INPUT_DIR in value:
        result.append(A_SOFTWARE)
    if ANOTHER_INPUT_DIR in value:
        result.append(ANOTHER_SOFTWARE)
    return result


class TestBaker(unittest.TestCase):

    def test_should_bake_softwares(self):
        mock_renderer = MagicMock()
        _bake(input_dirs=[AN_INPUT_DIR, ANOTHER_INPUT_DIR], output_dir=AN_OUTPUT_DIR,
                          renderer=mock_renderer, retrieve_software=mock_retrieve_software)
        self.assertCountEqual(mock_renderer.create_script.call_args_list,
                          [
                              call('AN_OUTPUT_DIR/artemis/wrappers', 'art', A_SOFTWARE, 'art'),
                              call('AN_OUTPUT_DIR/artemis/wrappers', 'act', A_SOFTWARE, 'act'),
                              call('AN_OUTPUT_DIR/gff3toembl/wrappers', 'interesting', ANOTHER_SOFTWARE, 'facts')])