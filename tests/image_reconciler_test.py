import unittest
from unittest.mock import MagicMock, call

from bakerlib.image_reconciler import ImageReconciler

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


class TestImageReconciler(unittest.TestCase):

    def setUp(self):
        self.mock_software_repository = MagicMock()
        self.mock_software_repository.get_software_catalog.return_value = [A_SOFTWARE, ANOTHER_SOFTWARE]

        self.mock_image_repo = MagicMock()
        self.mock_image_repo.get_images.return_value = [AN_IMAGE, ANOTHER_IMAGE]

        self.mock_comparator = MagicMock()
        self.under_test = ImageReconciler(self.mock_software_repository, self.mock_image_repo, self.mock_comparator)

    def test_should_delegate_reconcile_to_comparator(self):
        self.under_test.reconcile()
        self.assertCountEqual(self.mock_comparator.compare.call_args_list,
                              [call([A_SOFTWARE, ANOTHER_SOFTWARE], [AN_IMAGE, ANOTHER_IMAGE])])
