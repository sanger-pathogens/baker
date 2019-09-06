import unittest
from tempfile import NamedTemporaryFile, mkstemp
from os import remove
from bakerlib.file_processing import add_if_not_there

A_LINE = "A_LINE"
SOME_CONTENT = "SOME_CONTENT\n"
A_FIRST_PREFIX = "A_FIRST_PREFIX"
A_SECOND_PREFIX = "A_SECOND_PREFIX"
A_FIRST_SUFFIX = "A_FIRST_SUFFIX"
A_SECOND_SUFFIX = "A_SECOND_SUFFIX"


class TestFileProcessor(unittest.TestCase):

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for file in self.temp_files:
            try:
                remove(file)
            except:
                pass

    def test_should_create_file_if_inexistant(self):
        name = self._temp_file()
        add_if_not_there(name, A_LINE)
        self.assertFileContent(name, A_LINE + '\n')

    def test_should_add_prefix(self):
        name = self._temp_file()
        add_if_not_there(name, A_LINE, prefix=[
                         A_FIRST_PREFIX, A_SECOND_PREFIX])
        self.assertFileContent(name, A_FIRST_PREFIX +
                               '\n' + A_SECOND_PREFIX+'\n' + A_LINE + '\n')

    def test_should_add_suffix(self):
        name = self._temp_file()
        add_if_not_there(name, A_LINE, suffix=[
                         A_FIRST_SUFFIX, A_SECOND_SUFFIX])
        self.assertFileContent(name, A_LINE + '\n' +
                               A_FIRST_SUFFIX + '\n' + A_SECOND_SUFFIX + '\n')

    def test_should_add_to_end_of_file_if_exist(self):
        name = self._temp_file_with_content(SOME_CONTENT)
        add_if_not_there(name, A_LINE)
        self.assertFileContent(name, SOME_CONTENT + A_LINE + '\n')

    def _temp_file(self):
        (_, name) = mkstemp(text=True)
        self.temp_files.append(name)
        return name

    def _temp_file_with_content(self, content):
        name = self._temp_file()
        with open(name, 'w') as temp_file:
            temp_file.write(content)
        return name

    def assertFileContent(self, name, expected_content):
        actual_content = ""
        with open(name, 'r') as myfile:
            actual_content = myfile.read()
        self.assertEqual(actual_content, expected_content)
