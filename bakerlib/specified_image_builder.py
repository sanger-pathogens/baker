import logging

_logger = logging.getLogger('specified_image_builder')


class SpecifiedImageBuilder:
    def __init__(self, images, singularity_baker):
        self.images = images
        self.singularity_baker = singularity_baker

    def build_images(self):
        for image in self.images:
            _logger.debug("Building image %s" % image)
            self.singularity_baker.bake(image)

    def __call__(self):
        self.build_images()
