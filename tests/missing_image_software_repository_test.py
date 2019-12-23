import unittest
from unittest.mock import MagicMock

from bakerlib.missing_image_software_repository import MissingImageSoftwareRepository

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


class TestMissingImageSoftwareRepository(unittest.TestCase):
    def setUp(self):
        self.mock_software_repository = MagicMock()
        self.mock_software_repository.get_software_catalog.return_value = [A_SOFTWARE, ANOTHER_SOFTWARE]

        self.mock_image_repository = MagicMock()
        self.under_test = MissingImageSoftwareRepository(self.mock_software_repository, self.mock_image_repository)

    def test_should_return_empty_list_if_all_images_built(self):
        self.mock_image_repository.get_images.return_value = [AN_IMAGE, ANOTHER_IMAGE]
        actual = self.under_test.get_software_catalog()
        self.assertEqual(actual, [])

    def test_should_return_missing_images(self):
        self.mock_image_repository.get_images.return_value = [AN_IMAGE]
        actual = self.under_test.get_software_catalog()
        self.assertEqual(actual, [ANOTHER_SOFTWARE])

    def test_should_return_all_images_if_all_missing(self):
        self.mock_image_repository.get_images.return_value = []
        actual = self.under_test.get_software_catalog()
        self.assertCountEqual(actual, [A_SOFTWARE, ANOTHER_SOFTWARE])
