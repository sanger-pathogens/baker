class MissingImageSoftwareRepository:
    def __init__(self, software_repository, image_repository):
        self.software_repository = software_repository
        self.image_repository = image_repository

    def get_software_catalog(self):
        images = self.image_repository.get_images()
        catalog = self.software_repository.get_software_catalog()
        return [software for software in catalog if software["image"] not in images]
