import unittest
from unittest.mock import patch, mock_open

from bakerlib.softwares import get_softwares, _image_enrichment, _url_enrichments, _function_enrichments

AN_INPUT_DIR = 'AN INPUT DIRECTORY'
ANOTHER_INPUT_DIR = 'ANOTHER INPUT DIRECTORY'

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
    if value == ANOTHER_INPUT_DIR + "/*.yaml":
        return [ANOTHER_FILENAME]
    return []


class TestSoftwareRetrieval(unittest.TestCase):

    def test_should_copy_function_map(self):
        software = {
            "functions": [{"script_name": "script_name", "executable": "executable", "args": ["args1", "args2"]}]}
        expected = dict(software)
        expected["exported_functions"] = expected["functions"]
        _function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_populate_executable_in_function_if_missing(self):
        software = {"functions": [{"script_name": "script_name", "args": ["args1", "args2"]}]}
        expected = dict(software)
        expected["exported_functions"] = [
            {"script_name": "script_name", "executable": "script_name", "args": ["args1", "args2"]}]
        _function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_populate_args_in_function_if_missing(self):
        software = {"functions": [{"script_name": "script_name", "executable": "executable"}]}
        expected = dict(software)
        expected["exported_functions"] = [{"script_name": "script_name", "executable": "executable", "args": []}]
        _function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_populate_simple_function_if_string(self):
        software = {"functions": ["script_name"]}
        expected = dict(software)
        expected["exported_functions"] = [{"script_name": "script_name", "executable": "script_name", "args": []}]
        _function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_combine_styles(self):
        software = {"functions": ["script_name", {"script_name": "script_name2"}]}
        expected = dict(software)
        expected["exported_functions"] = [{"script_name": "script_name", "executable": "script_name", "args": []},
                                          {"script_name": "script_name2", "executable": "script_name2", "args": []}]
        _function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_enrich_software_with_image(self):
        software = {"name": "A_NAME", "version": "A_VERSION"}
        expected = dict(software)
        expected["image"] = "A_NAME-A_VERSION.simg"
        _image_enrichment(software)
        self.assertEqual(software, expected)

    def test_should_not_enrich_software_with_image_if_already_there(self):
        software = {"name": "A_NAME", "version": "A_VERSION", "image": "AN_IMAGE"}
        expected = dict(software)
        _image_enrichment(software)
        self.assertEqual(software, expected)

    def test_should_enrich_software_with_name_and_version(self):
        software = {"url": "docker://someserver/name:version"}
        expected = dict(software)
        expected["name"] = "name"
        expected["version"] = "version"
        _url_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_enrich_software_with_version_only(self):
        software = {"url": "docker://someserver/name:version", "name": "A_NAME"}
        expected = dict(software)
        expected["version"] = "version"
        _url_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_enrich_software_with_name_only(self):
        software = {"url": "docker://someserver/name:version", "version": "A_VERSION"}
        expected = dict(software)
        expected["name"] = "name"
        _url_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_not_enrich_software_with_name_and_version_if_already_set(self):
        software = {"url": "docker://someserver/name:version", "name": "A_NAME", "version": "A_VERSION"}
        expected = dict(software)
        _url_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_get_softwares(self):
        with patch('glob.glob', side_effect=glob_side_effect) as mock_glob:
            with patch("builtins.open", mock_open(read_data=A_YAML_CONTENT)) as mo:
                handlers = (mo.return_value, mock_open(
                    read_data=ANOTHER_YAML_CONTENT).return_value)
                mo.side_effect = handlers
                softwares = get_softwares([AN_INPUT_DIR, ANOTHER_INPUT_DIR], enrichments=[])
                self.assertEqual(mock_glob.call_count, 4)
                print(softwares)
                print([A_SOFTWARE, ANOTHER_SOFTWARE])
                self.assertCountEqual(softwares, [A_SOFTWARE, ANOTHER_SOFTWARE])

    def test_should_return_no_software_if_no_files(self):
        with patch('glob.glob', side_effect=lambda t: []) as mock_glob:
            softwares = get_softwares([AN_INPUT_DIR, ANOTHER_INPUT_DIR], enrichments=[])
            self.assertEqual(mock_glob.call_count, 4)
            self.assertEqual(softwares, [])

    def test_should_skip_invalid_yaml(self):
        with patch('glob.glob', side_effect=glob_side_effect) as mock_glob:
            with patch("builtins.open", mock_open(read_data=INVALID_YAML)) as mo:
                handlers = (mo.return_value, mock_open(
                    read_data=ANOTHER_YAML_CONTENT).return_value)
                mo.side_effect = handlers
                softwares = get_softwares([AN_INPUT_DIR, ANOTHER_INPUT_DIR], enrichments=[])
                self.assertEqual(mock_glob.call_count, 4)
                self.assertCountEqual(softwares, [ANOTHER_SOFTWARE])
