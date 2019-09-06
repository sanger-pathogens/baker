import logging
from subprocess import run
from os import makedirs

from bakerlib.file_processing import add_if_not_there

_logger = logging.getLogger('softwares')

def update_rc_file(directory, filename, wrapper_dir):
    full_path = directory+"/"+filename
    makedirs(directory, exist_ok=True)
    add_if_not_there(full_path, "add_to_path ${PATHOGEN_ETC_DIR}/" + wrapper_dir, prefix=[
                     "# Adding wrapper scripts to PATH"], suffix=[""])
    run(["chmod", "-R", "444", full_path])
    _logger.debug("Created rc file %s", full_path)
