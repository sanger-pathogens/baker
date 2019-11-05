import unittest
from unittest.mock import MagicMock, call

from bakerlib.image_comparator import ImageComparator

AN_IMAGE = "AN_IMAGE"
ANOTHER_IMAGE = "ANOTHER_IMAGE"

A_SOFTWARE = {
    "name": "artemis",
    "version": "18.0.3",
    "docker_image": "sangerpathogens/artemis:release-v18.0.3",
    "image": AN_IMAGE
}

ANOTHER_SOFTWARE = {
    "url": "docker://someurl/gff3toembl:1.1.4",
    "name": "gff3toembl",
    "version": "1.1.4",
    "image": ANOTHER_IMAGE
}


class TestImageComparator(unittest.TestCase):

    def setUp(self):
        self.mock_missing = MagicMock()
        self.mock_unknown = MagicMock()
        self.under_test = ImageComparator(self.mock_missing, self.mock_unknown)

    def test_should_compare_software_and_images_no_difference(self):
        self.under_test.compare([A_SOFTWARE, ANOTHER_SOFTWARE], [AN_IMAGE, ANOTHER_IMAGE])
        self.assertEqual(self.mock_missing.call_count, 0)
        self.assertEqual(self.mock_unknown.call_count, 0)

    def test_should_compare_software_and_images_unknown_image(self):
        self.under_test.compare([A_SOFTWARE], [AN_IMAGE, ANOTHER_IMAGE])
        self.assertEqual(self.mock_missing.call_count, 0)
        self.assertCountEqual(self.mock_unknown.call_args_list, [call(ANOTHER_IMAGE)])

    def test_should_compare_software_and_images_missing_image(self):
        self.under_test.compare([A_SOFTWARE, ANOTHER_SOFTWARE], [AN_IMAGE])
        self.assertCountEqual(self.mock_missing.call_args_list, [call(ANOTHER_IMAGE)])
        self.assertEqual(self.mock_unknown.call_count, 0)

    def test_should_compare_software_and_images_both_unknown_and_missing_images(self):
        self.under_test.compare([A_SOFTWARE], [ANOTHER_IMAGE])
        self.assertCountEqual(self.mock_missing.call_args_list, [call(AN_IMAGE)])
        self.assertCountEqual(self.mock_unknown.call_args_list, [call(ANOTHER_IMAGE)])
