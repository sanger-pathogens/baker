import unittest
from unittest.mock import patch, call, mock_open
from bakerlib.docker_config import DockerConfigError, DockerConfig


AN_INPUT_DIR = 'AN INPUT DIRECTORY'
ANOTHER_INPUT_DIR = 'ANOTHER INPUT DIRECTORY'

A_FILENAME = "A FILENAME.yml"
ANOTHER_FILENAME = "ANOTHER FILENAME.yaml"

A_YAML_CONTENT = '''
an_unused_url:
- some other command
someurl:
- some command
- another command
    '''
INVALID_YAML = "\tinvalid:\ninvalid\n"

A_SOFTWARE = {
    "url": "docker://someurl/name:version",
    "custom_init": "some init",
    "functions": ['function1', 'function2']}

ANOTHER_SOFTWARE = {
    "url": "docker://someurl2/othername:otherversion",
    "name": "A_NAME",
    "version": "A_VERSION",
    "custom_init": "some init2",
    "functions": ['function4', 'function5']}

YET_ANOTHER_SOFTWARE = {
    "url": "not_docker://someurl2/othername:otherversion",
    "functions": ['function4', 'function5']}

class TestDockerConfig(unittest.TestCase):

    def test_should_get_environment_if_exists(self):
        with patch("builtins.open", mock_open(read_data=A_YAML_CONTENT)) as mo:
            handlers = (mo.return_value, mock_open(
                read_data=A_YAML_CONTENT).return_value)
            mo.side_effect = handlers
            config = DockerConfig(A_FILENAME)
            self.assertEqual(config.environment_for(A_SOFTWARE), ["some command", "another command"])
            self.assertCountEqual(mo.call_args_list, [call(A_FILENAME, 'r')])

    def test_should_get_empty_environment_if_doesnt_exists(self):
        with patch("builtins.open", mock_open(read_data=A_YAML_CONTENT)) as mo:
            handlers = (mo.return_value, mock_open(
                read_data=A_YAML_CONTENT).return_value)
            mo.side_effect = handlers
            config = DockerConfig(A_FILENAME)
            self.assertEqual(config.environment_for(ANOTHER_SOFTWARE), [])
            self.assertCountEqual(mo.call_args_list, [call(A_FILENAME, 'r')])

    def test_should_get_empty_environment_if_not_docker_url(self):
        with patch("builtins.open", mock_open(read_data=A_YAML_CONTENT)) as mo:
            handlers = (mo.return_value, mock_open(
                read_data=A_YAML_CONTENT).return_value)
            mo.side_effect = handlers
            config = DockerConfig(A_FILENAME)
            self.assertEqual(config.environment_for(YET_ANOTHER_SOFTWARE), [])
            self.assertCountEqual(mo.call_args_list, [call(A_FILENAME, 'r')])
