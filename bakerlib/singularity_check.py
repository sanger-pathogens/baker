class SingularityChecker:

    def __init__(self, missing_image_call=lambda s: None, unknown_image_call=lambda s: None):
        self.missing_image_call = missing_image_call
        self.unknown_image_call = unknown_image_call

    def check(self, softwares, images):
        softwares_images = [software["image"] for software in softwares]
        missing_images = {i for i in softwares_images if i not in images}
        unknown_images = {i for i in images if i not in softwares_images}
        for m in missing_images:
            self.missing_image_call(m)
        for u in unknown_images:
            self.unknown_image_call(u)
