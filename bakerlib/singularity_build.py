from logging import getLogger
import subprocess

_logger = getLogger("singularity_exec")

class SingularityBakingError(Exception):
    pass


class SingularityExecutor:

    def execute(self, outdir, config, software):
        output_image = "%s/%s" % (outdir, software["image"])
        environment = "" if config == [] else ';'.join(config) + ';' 
        command = "rm -f '%s';%ssingularity build '%s' '%s'" % (output_image, environment, output_image, software["url"])
        _logger.debug("Executing command: %s" % command)
        self._shell(command)
        _logger.debug("Built image: %s", output_image)

    def _shell(self, command):
        p = subprocess.Popen(command, shell=True)
        p.wait()

class SingularityBaker:

    def __init__(self, outdir, config, softwares, executor=SingularityExecutor()):
        self.outdir = outdir
        self.config = config
        self.softwares = {software["image"]:software for software in softwares}
        self.executor = executor

    def bake(self, image):
        software = self.softwares.get(image)
        if software is None:
            raise SingularityBakingError("Could not find software for image " + image)
        config = self.config.environment_for(software)
        self.executor.execute(self.outdir, config, software)
