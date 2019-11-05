class ImageComparator:

    def __init__(self, missing_image_call=lambda s: None, unknown_image_call=lambda s: None):
        self.missing_image_call = missing_image_call
        self.unknown_image_call = unknown_image_call

    def compare(self, software_catalog, images):
        image_names = [software["image"] for software in software_catalog]
        missing_images = {i for i in image_names if i not in images}
        unknown_images = {i for i in images if i not in image_names}
        for m in missing_images:
            self.missing_image_call(m)
        for u in unknown_images:
            self.unknown_image_call(u)
