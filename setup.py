import os

from setuptools import setup

NAME = "entrypoint2"

# get __version__
__version__ = None
exec(open(os.path.join(NAME, "about.py")).read())
VERSION = __version__

URL = "https://github.com/ponty/entrypoint2"
DESCRIPTION = "easy to use command-line interface for python modules"
LONG_DESCRIPTION = """easy to use command-line interface for Python modules

home: https://github.com/ponty/entrypoint2/tree/"""
LONG_DESCRIPTION += VERSION

PACKAGES = [
    NAME,
    NAME + ".examples",
]

classifiers = [
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

install_requires = []

# compatible with distutils of python 2.3+ or later
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    classifiers=classifiers,
    keywords="argparse decorator optparse signature command-line",
    author="ponty",
    # author_email='',
    url=URL,
    license="BSD",
    packages=PACKAGES,
    # include_package_data=True,
    # zip_safe=False,
    install_requires=install_requires,
    # **extra
)
