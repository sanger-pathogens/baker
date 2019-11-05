import unittest

from bakerlib.software_enrichments import url_enrichments, function_enrichments, image_enrichment, \
    software_name_version_validation
from bakerlib.software_repository import InvalidSoftwareError

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


class TestFunctionEnrichment(unittest.TestCase):

    def test_should_copy_function_map(self):
        software = {
            "functions": [{"script_name": "script_name", "executable": "executable", "args": ["args1", "args2"]}]}
        expected = dict(software)
        expected["exported_functions"] = expected["functions"]
        function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_populate_executable_in_function_if_missing(self):
        software = {"functions": [{"script_name": "script_name", "args": ["args1", "args2"]}]}
        expected = dict(software)
        expected["exported_functions"] = [
            {"script_name": "script_name", "executable": "script_name", "args": ["args1", "args2"]}]
        function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_populate_args_in_function_if_missing(self):
        software = {"functions": [{"script_name": "script_name", "executable": "executable"}]}
        expected = dict(software)
        expected["exported_functions"] = [{"script_name": "script_name", "executable": "executable", "args": []}]
        function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_populate_simple_function_if_string(self):
        software = {"functions": ["script_name"]}
        expected = dict(software)
        expected["exported_functions"] = [{"script_name": "script_name", "executable": "script_name", "args": []}]
        function_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_combine_styles(self):
        software = {"functions": ["script_name", {"script_name": "script_name2"}]}
        expected = dict(software)
        expected["exported_functions"] = [{"script_name": "script_name", "executable": "script_name", "args": []},
                                          {"script_name": "script_name2", "executable": "script_name2", "args": []}]
        function_enrichments(software)
        self.assertEqual(software, expected)


class TestImageEnrichment(unittest.TestCase):

    def test_should_enrich_software_with_image(self):
        software = {"name": "A_NAME", "version": "A_VERSION"}
        expected = dict(software)
        expected["image"] = "A_NAME-A_VERSION.simg"
        image_enrichment(software)
        self.assertEqual(software, expected)

    def test_should_not_enrich_software_with_image_if_already_there(self):
        software = {"name": "A_NAME", "version": "A_VERSION", "image": "AN_IMAGE"}
        expected = dict(software)
        image_enrichment(software)
        self.assertEqual(software, expected)


class TestUrlEnrichment(unittest.TestCase):

    def test_should_enrich_software_with_name_and_version(self):
        software = {"url": "docker://someserver/name:version"}
        expected = dict(software)
        expected["name"] = "name"
        expected["version"] = "version"
        url_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_enrich_software_with_version_only(self):
        software = {"url": "docker://someserver/name:version", "name": "A_NAME"}
        expected = dict(software)
        expected["version"] = "version"
        url_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_enrich_software_with_name_only(self):
        software = {"url": "docker://someserver/name:version", "version": "A_VERSION"}
        expected = dict(software)
        expected["name"] = "name"
        url_enrichments(software)
        self.assertEqual(software, expected)

    def test_should_not_enrich_software_with_name_and_version_if_already_set(self):
        software = {"url": "docker://someserver/name:version", "name": "A_NAME", "version": "A_VERSION"}
        expected = dict(software)
        url_enrichments(software)
        self.assertEqual(software, expected)


class TestNameVersionValidation(unittest.TestCase):

    def test_pass_if_name_and_version(self):
        software = {"name": "a_name", "version": "ok"}
        software_name_version_validation(software)

    def test_fail_if_name_missing(self):
        software = {"version": "ok"}
        with self.assertRaises(InvalidSoftwareError) as _:
            software_name_version_validation(software)

    def test_fail_if_version_missing(self):
        software = {"name": "a_name"}
        with self.assertRaises(InvalidSoftwareError) as _:
            software_name_version_validation(software)
