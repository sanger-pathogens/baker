import unittest
import os
import argparse
import scripts

from unittest.mock import patch, call
from bakerlib.main import bake


AN_INPUT_DIR = 'AN INPUT DIRECTORY'
ANOTHER_INPUT_DIR = 'ANOTHER INPUT DIRECTORY'
A_SOFTWARE = {"url":"a_URL"}
ANOTHER_SOFTWARE = {"url":"another_URL"}
AN_OUTPUT_DIR = "AN_OUTPUT_DIR"

def glob_side_effect(value): 
    result = []
    if AN_INPUT_DIR in value:
        result.append(A_SOFTWARE)
    if ANOTHER_INPUT_DIR in value:
        result.append(ANOTHER_SOFTWARE)
    return result

class TestBaker(unittest.TestCase):

    def test_should_bake_softwares(self):
        with patch('bakerlib.main.get_softwares', side_effect=glob_side_effect) as mock_glob:
            result = bake(input_dirs=[AN_INPUT_DIR,ANOTHER_INPUT_DIR], output_dir=AN_OUTPUT_DIR)
            self.assertCountEqual(result, [A_SOFTWARE, ANOTHER_SOFTWARE])