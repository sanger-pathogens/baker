import unittest
from unittest.mock import MagicMock, call

from bakerlib.specified_image_builder import SpecifiedImageBuilder

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


class TestSpecifiedImageBuilder(unittest.TestCase):

    def setUp(self):
        self.mock_baker = MagicMock()
        self.under_test = SpecifiedImageBuilder([AN_IMAGE, ANOTHER_IMAGE], self.mock_baker)

    def test_should_build_images(self):
        self.under_test.build_images()
        self.assertCountEqual(self.mock_baker.bake.call_args_list, [call(AN_IMAGE), call(ANOTHER_IMAGE)])
