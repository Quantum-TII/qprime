# Installation script for python
from setuptools import setup, find_packages
import os
import re


PACKAGE = 'qprime'


def get_version():
    """ Gets the version from the package's __init__ file
    if there is some problem, let it happily fail """
    VERSIONFILE = os.path.join(PACKAGE, '__init__.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)


setup(name=PACKAGE,
      version=get_version(),
      description='qbit states from prime numbers',
      author = 'Stefano Carrazza',
      author_email='stefano.carrazza@cern.ch',
      url='https://github.com/Quantum-TII/qprime',
      packages=find_packages(PACKAGE),
      zip_safe=False,
      classifiers=[
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Physics',
      ],
      install_requires=[
          'numpy',
          'numba>=0.47',
          'tensorflow>=2',
      ],
      python_requires='>=3.6'
)
