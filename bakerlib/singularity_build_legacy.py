import subprocess
from logging import getLogger

from jinja2 import Environment, FileSystemLoader

_logger = getLogger("singularity_legacy")


class SingularityLegacyBakingError(Exception):
    pass


class SingularityLegacyBaker:

    def __init__(self, outdir, template_dir, software_repository, images):
        self.outdir = outdir
        self.template_dir = template_dir
        self.software_map = {software["image"]: software for software in software_repository.get_software_catalog()}
        self.images = images

    def bake_all(self):
        _logger.debug("Building images %s" % self.images)
        for image in self.images:
            self._bake(image)

    def __call__(self):
        self.bake_all()

    def _bake(self, image):
        software = self.software_map.get(image)
        if software is None:
            raise SingularityLegacyBakingError("Could not find software for image " + image)

        output_image = "%s/%s" % (self.outdir, software["image"])
        recipe = output_image + '.recipe'
        env = Environment(
            loader=FileSystemLoader(self.template_dir)
        )
        with open(recipe, 'w') as recipe_file:
            template = env.get_template(software['template'])
            print(template.render(software), file=recipe_file)

        self._shell("rm -f '%s';singularity build --fakeroot '%s' '%s'" % (output_image, output_image, recipe))
        _logger.debug("Built image: %s", output_image)

    @staticmethod
    def _shell(command):
        p = subprocess.Popen(command, shell=True)
        p.wait()
        if p.returncode != 0:
            raise SingularityLegacyBakingError("singularity process failed while building %s" % command)
