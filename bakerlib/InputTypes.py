import os
import argparse

class InputTypes:

   def is_foo_valid(whatever):
      if len(str(whatever)) < 3:
         raise argparse.ArgumentTypeError("'foo' must contain at least 3 chars")
         return False
      return whatever
