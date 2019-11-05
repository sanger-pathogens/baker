import unittest
from unittest.mock import patch

from bakerlib.images import ImageRepository

AN_OUTPUT_DIR = 'AN INPUT DIRECTORY'

AN_IMAGE = "software-version.simg"
ANOTHER_IMAGE = "other-software-version.sif"


def glob_side_effect(value):
    if value == AN_OUTPUT_DIR + "/*.simg":
        return [AN_OUTPUT_DIR + '/' + AN_IMAGE]
    if value == AN_OUTPUT_DIR + "/*.sif":
        return [AN_OUTPUT_DIR + '/' + ANOTHER_IMAGE]
    return []


class TestImageRepository(unittest.TestCase):
    def setUp(self):
        self.under_test = ImageRepository(AN_OUTPUT_DIR)

    def test_should_get_images(self):
        with patch('glob.glob', side_effect=glob_side_effect) as mock_glob:
            actual = self.under_test.get_images()
            self.assertGreaterEqual(mock_glob.call_count, 1)
            self.assertCountEqual(actual, [AN_IMAGE, ANOTHER_IMAGE])

    def test_should_return_no_software_if_no_files(self):
        with patch('glob.glob', side_effect=lambda t: []) as mock_glob:
            actual = self.under_test.get_images()
            self.assertGreaterEqual(mock_glob.call_count, 1)
            self.assertEqual(actual, [])
