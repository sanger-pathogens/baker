from logging import getLogger
from jinja2 import Environment, FileSystemLoader
import subprocess

_logger = getLogger("singularity_legacy")

class SingularityLegacyBakingError(Exception):
    pass

class SingularityLegacyBaker:

    def __init__(self, outdir, template_dir, softwares):
        self.outdir = outdir
        self.template_dir = template_dir
        self.softwares = {software["image"]:software for software in softwares}

    def bake(self, image):
        software = self.softwares.get(image)
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

    def _shell(self, command):
        p = subprocess.Popen(command, shell=True)
        p.wait()
