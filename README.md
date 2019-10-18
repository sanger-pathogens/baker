# baker
Baker is a tool that facilitates the installation and management of bioinformatics software.  It leverages container technology such as singularity and docker as well as Jinja2 template to build wrapper scripts and singularity images

[![Build Status](https://travis-ci.org/sanger-pathogens/baker.svg?branch=master)](https://travis-ci.org/sanger-pathogens/baker)   
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/sanger-pathogens/baker/blob/master/LICENSE)   
[![Docker Build Status](https://img.shields.io/docker/cloud/build/sangerpathogens/baker.svg)](https://hub.docker.com/r/sangerpathogens/baker)   
[![Docker Pulls](https://img.shields.io/docker/pulls/sangerpathogens/baker.svg)](https://hub.docker.com/r/sangerpathogens/baker)   
[![codecov](https://codecov.io/gh/sanger-pathogens/baker/branch/master/graph/badge.svg)](https://codecov.io/gh/sanger-pathogens/baker)   

## Install
### Pip
Install master:
```
pip install git+https://github.com/sanger-pathogens/baker.git
```
Install a specific version:```pip install git+https://github.com/sanger-pathogens/baker.git@<TAG>```.  Example:
```
pip install git+https://github.com/sanger-pathogens/baker.git@v0.0.1
```
Once install, baker can be run directly:
```
baker.py -h
```
### Docker
Pull the latest image:
```
docker pull sangerpathogens/baker:latest
```

Run in a container:
```
docker run --rm -it -v /home:/home sangerpathogens/baker:latest baker.py -h
```

To pull and run a specific version, just replace ```latest``` by the version number.  Example:
```
docker pull sangerpathogens/baker:0.0.1
docker run --rm -it -v /home:/home sangerpathogens/baker:0.0.1 baker.py -h
```

## Usage
Please run ```baker.py -h``` for help

## License
Baker is free software, licensed under [GPLv3](https://github.com/sanger-pathogens/baker/blob/master/LICENSE).

