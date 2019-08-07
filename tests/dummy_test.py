import unittest
import os

#test_modules_dir = os.path.dirname(os.path.realpath(__file__))
#data_dir = os.path.join(test_modules_dir, 'data','read')

class TestRead(unittest.TestCase):

   def test_initialise(self):
      testvalue = 'foo'
      self.assertEqual(testvalue, 'foo')
