import logging

_logger = logging.getLogger('missing_image_builder')


class MissingImageBuilder:
    def __init__(self, software_catalog, image_repo, checker):
        self.software_catalog = software_catalog
        self.image_repo = image_repo
        self.checker = checker

    def check(self):
        images = self.image_repo.get_images()
        _logger.debug("Building missing images...")
        self.checker.check(self.software_catalog, images)

    def __call__(self):
        self.check()
