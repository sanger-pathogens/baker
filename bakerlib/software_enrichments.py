import re

from bakerlib.software_repository import InvalidSoftwareError


def url_enrichments(software):
    if "url" in software:
        pattern = re.compile("^docker://.+/(?P<name>[^:]+):(?P<version>[^:]+)")
        match = pattern.search(software["url"])
        if match is not None:
            if "name" not in software:
                software["name"] = match.group("name")
            if "version" not in software:
                software["version"] = match.group("version")


def software_name_version_validation(software):
    if "name" not in software:
        raise InvalidSoftwareError("Name not in software %s" % software)
    if "version" not in software:
        raise InvalidSoftwareError("Version not in software %s" % software)


def function_enrichments(software):
    exported_functions = []
    for function in software["functions"]:
        if isinstance(function, dict):
            if "args" not in function:
                function["args"] = []
            if "executable" not in function:
                function["executable"] = function["script_name"]
            exported_functions.append(function)
        elif isinstance(function, str):
            exported_functions.append({"script_name": function, "executable": function, "args": []})
    software["exported_functions"] = exported_functions


def image_enrichment(software):
    if "image" not in software:
        software["image"] = software['name'] + \
                            '-' + software['version'] + '.simg'
