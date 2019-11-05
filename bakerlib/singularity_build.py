from logging import getLogger
from subprocess import Popen

_logger = getLogger("singularity_exec")


class SingularityBakingError(Exception):
    pass


class SingularityExecutor:

    def execute(self, outdir, config, software):
        output_image = "%s/%s" % (outdir, software["image"])
        environment = "" if config == [] else ';'.join(config) + ';'
        command = "rm -f '%s';%ssingularity build '%s' '%s'" % (
            output_image, environment, output_image, software["url"])
        _logger.debug("Executing command: %s" % command)
        self._shell(command)
        _logger.debug("Built image: %s", output_image)

    @staticmethod
    def _shell(command):
        p = Popen(command, shell=True)
        p.wait()
        if p.returncode != 0:
            raise SingularityBakingError("singularity process failed while building %s" % command)


class SingularityBaker:

    def __init__(self, output_dir, config, software_repository, executor):
        catalog = software_repository.get_software_catalog()
        self.output_dir = output_dir
        self.config = config
        self.software_map = {software["image"]: software for software in catalog}
        self.executor = executor

    def bake(self, image):
        software = self.software_map.get(image)
        if software is None:
            raise SingularityBakingError("Could not find software for image " + image)
        config = self.config.environment_for(software)
        self.executor.execute(self.output_dir, config, software)
