from re import compile

from yaml import load, SafeLoader, YAMLError


class DockerConfigError(Exception):
    pass


class DockerConfig:

    def __init__(self, config):
        try:
            with open(config, 'r') as input:
                self.environments = load(input, Loader=SafeLoader)
        except YAMLError:
            raise DockerConfigError("Could not load yaml " + config)

    def environment_for(self, software):
        pattern = compile("^docker://(?P<server>[^/:]+).*$")
        match = pattern.search(software["url"])
        empty_env = []
        if match is not None:
            server = match.group("server")
            return self.environments.get(server, empty_env)
        return empty_env
