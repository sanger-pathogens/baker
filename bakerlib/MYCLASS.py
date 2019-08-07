import logging
import os
import sys
import time

class MYCLASS:
   def __init__(self,options):
      self.logger = logging.getLogger(__name__)
      self.verbose                    = options.verbose
      self.output_file                = options.output_file
      
      if self.output_file and os.path.exists(self.output_file):
         self.logger.error("The output file already exists, please choose another filename: "+ self.output_file)
         sys.exit(1)
               
      if self.verbose:
         self.logger.setLevel(logging.DEBUG)
      else:
         self.logger.setLevel(logging.ERROR)
         
   def run(self):
      print(__name__+".run() was called")
