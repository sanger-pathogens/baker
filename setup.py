import os
import shutil
import sys
import glob
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = 'x.y.z'
if os.path.exists('VERSION'):
  version = open('VERSION').read().strip()

setup(
    name='baker',
    version=version,
    description='What Tim did next',
	  long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages = ["bakerlib"],
    author='Olivier Seret',
    author_email='path-help@sanger.ac.uk',
    url='https://github.com/sanger-pathogens/baker',
    scripts=glob.glob('scripts/*'),
    setup_requires=['nose>=1.3'],
    test_suite='nose.collector',
    tests_require=['nose >= 1.3'],
    install_requires=[
      'PyYaml >= 5.1',
      'Jinja2 >= 2.10.1'
       ],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience  :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)
