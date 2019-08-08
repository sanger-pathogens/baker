import unittest
from unittest.mock import patch, call, mock_open
from bakerlib.softwares import get_softwares
from io import StringIO


AN_INPUT_DIR = 'AN INPUT DIRECTORY'
ANOTHER_INPUT_DIR = 'ANOTHER INPUT DIRECTORY'

A_FILENAME = "A FILENAME.yml"
ANOTHER_FILENAME = "ANOTHER FILENAME.yaml"

A_YAML_CONTENT = '''
url: docker://someurl
custom_init: some init
functions:
- function1
- function2
    '''
ANOTHER_YAML_CONTENT = '''
url: docker://someurl2
custom_init: some init2
functions:
    - function4
    - function5
        '''
INVALID_YAML = "\tinvalid:\ninvalid\n"

A_SOFTWARE = {
    "url": "docker://someurl",
    "custom_init": "some init",
    "functions": ['function1', 'function2']}

ANOTHER_SOFTWARE = {
    "url": "docker://someurl2",
    "custom_init": "some init2",
    "functions": ['function4', 'function5']}

def glob_side_effect(value): 
    if value == AN_INPUT_DIR + "/*.yml":
            return [A_FILENAME]
    if value == ANOTHER_INPUT_DIR + "/*.yaml":
        return [ANOTHER_FILENAME]
    return []
        

class TestSoftwareRetrieval(unittest.TestCase):

    def setUp(self):
        pass
        #self.under_test = Bake(self.an_output_directory)

    def test_should_get_softwares(self):
        with patch('glob.glob', side_effect=glob_side_effect) as mock_glob:
            with patch("builtins.open", mock_open(read_data=A_YAML_CONTENT)) as mo:
                handlers = (mo.return_value, mock_open(
                    read_data=ANOTHER_YAML_CONTENT).return_value)
                mo.side_effect = handlers
                softwares = get_softwares([AN_INPUT_DIR, ANOTHER_INPUT_DIR])
                self.assertEqual(mock_glob.call_count, 4)
                self.assertCountEqual(softwares, [A_SOFTWARE, ANOTHER_SOFTWARE])

    def test_should_return_no_software_if_no_files(self):
        with patch('glob.glob', side_effect=lambda t: []) as mock_glob:
            softwares = get_softwares([AN_INPUT_DIR, ANOTHER_INPUT_DIR])
            self.assertEqual(mock_glob.call_count, 4)
            self.assertEqual(softwares, [])

    def test_should_skip_invalid_yaml(self):
        with patch('glob.glob', side_effect=glob_side_effect) as mock_glob:
            with patch("builtins.open", mock_open(read_data=INVALID_YAML)) as mo:
                handlers = (mo.return_value, mock_open(
                    read_data=ANOTHER_YAML_CONTENT).return_value)
                mo.side_effect = handlers
                softwares = get_softwares([AN_INPUT_DIR, ANOTHER_INPUT_DIR])
                self.assertEqual(mock_glob.call_count, 4)
                self.assertCountEqual(softwares, [ANOTHER_SOFTWARE])
