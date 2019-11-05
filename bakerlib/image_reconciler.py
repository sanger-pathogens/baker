import logging

_logger = logging.getLogger('missing_image_builder')


class ImageReconciler:
    def __init__(self, software_repository, image_repo, comparator):
        self.software_repository = software_repository
        self.image_repo = image_repo
        self.comparator = comparator

    def reconcile(self):
        images = self.image_repo.get_images()
        catalog = self.software_repository.get_software_catalog()
        self.comparator.compare(catalog, images)

    def __call__(self):
        self.reconcile()
