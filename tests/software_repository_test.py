import unittest
from unittest.mock import patch, mock_open

from bakerlib.software_repository import SoftwareRepository

AN_INPUT_DIR = 'AN INPUT DIRECTORY'

A_FILENAME = "A FILENAME.yml"
ANOTHER_FILENAME = "ANOTHER FILENAME.yaml"

A_YAML_CONTENT = '''
url: docker://someurl/name:version
custom_init: some init
functions:
- function1
- function2
    '''
ANOTHER_YAML_CONTENT = '''
url: docker://someurl2
name: A_NAME
version: A_VERSION
custom_init: some init2
functions:
    - function4
    - function5
        '''
INVALID_YAML = "\tinvalid:\ninvalid\n"

A_SOFTWARE = {
    "url": "docker://someurl/name:version",
    "custom_init": "some init",
    "functions": ['function1', 'function2']}

ANOTHER_SOFTWARE = {
    "url": "docker://someurl2",
    "name": "A_NAME",
    "version": "A_VERSION",
    "custom_init": "some init2",
    "functions": ['function4', 'function5']}

ANOTHER_SOFTWARE_ENRICHED = {
    "url": "docker://someurl2",
    "name": "A_NAME",
    "version": "A_VERSION",
    "image": "A_NAME-A_VERSION.simg",
    "custom_init": "some init2",
    "functions": ['function4', 'function5']}


def glob_side_effect(value):
    if value == AN_INPUT_DIR + "/*.yml":
        return [A_FILENAME]
    if value == AN_INPUT_DIR + "/*.yaml":
        return [ANOTHER_FILENAME]
    return []


class TestSoftwareRetrieval(unittest.TestCase):

    def setUp(self):
        self.under_test = SoftwareRepository(AN_INPUT_DIR, [])

    def test_should_get_softwares(self):
        with patch('glob.glob', side_effect=glob_side_effect) as _:
            with patch("builtins.open", mock_open(read_data=A_YAML_CONTENT)) as mo:
                handlers = (mo.return_value, mock_open(
                    read_data=ANOTHER_YAML_CONTENT).return_value)
                mo.side_effect = handlers
                software_catalog = self.under_test.get_software_catalog()
                self.assertCountEqual(software_catalog, [A_SOFTWARE, ANOTHER_SOFTWARE])

    def test_should_return_no_software_if_no_files(self):
        with patch('glob.glob', side_effect=lambda t: []) as _:
            software_catalog = self.under_test.get_software_catalog()
            self.assertEqual(software_catalog, [])

    def test_should_skip_invalid_yaml(self):
        with patch('glob.glob', side_effect=glob_side_effect) as _:
            with patch("builtins.open", mock_open(read_data=INVALID_YAML)) as mo:
                handlers = (mo.return_value, mock_open(
                    read_data=ANOTHER_YAML_CONTENT).return_value)
                mo.side_effect = handlers
                software_catalog = self.under_test.get_software_catalog()
                self.assertCountEqual(software_catalog, [ANOTHER_SOFTWARE])
