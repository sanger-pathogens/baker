import glob
import ntpath
import logging

_logger = logging.getLogger('softwares')

class ImageRepository:
    def __init__(self, directory):
        self.directory = directory

    def get_images(self):
        _logger.debug("Researching images in directory %s" % self.directory)
        files = glob.glob(self.directory + '/*.simg') + glob.glob(self.directory + '/*.sif')
        results = [ntpath.basename(f) for f in files]
        _logger.debug("Find following images: %s" % results)
        return results


        

