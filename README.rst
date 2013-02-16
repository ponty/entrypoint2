entrypoint2 is an easy to use argparse_ based command-line interface for python modules, fork of `entrypoint <http://pypi.python.org/pypi/entrypoint/>`_. 
It translates function signature and documentation to argparse_ configuration.


Links:

 * home: https://github.com/ponty/entrypoint2
 * documentation: http://ponty.github.com/entrypoint2

Goals:

 - simplicity: only one decorator to add to existing code
 
Features:

 - good for protoyping or simple CLI
 - generate CLI parameters from function signature 
 - generate CLI documentation from python documentation 
 - the decorated function has the same behavior as without the entrypoint2 decorator
 - boolean parameters are toggle flags (e.g. ``--verbose``) 
 - function signature is preserved so it can be called both from command-line and external module
 - function name, doc and module are preserved so it can be used with sphinx autodoc_
 - sphinx autodoc_ documentation style is supported: ``:param x: this is x``
 - automatic ``--version`` flag, which prints version variable from the current module
   (``__version__``, ``VERSION``, ..) 
 - automatic ``--debug`` flag, which turns on logging 
 - short flags are generated from long flags automatically (e.g. ``--parameter`` -> ``-p``) 
 - unit tests
 - supported python versions: 2.5, 2.6, 2.7, 3.1, 3.2, PyPy
 - support for repeating arguments
 
Known problems:
 - None. 

Similar projects:

 * `entrypoint <http://pypi.python.org/pypi/entrypoint/>`_
 * `plac  <http://micheles.googlecode.com/hg/plac/doc/plac.html>`_
 * `baker <http://bitbucket.org/mchaput/baker>`_   
 * `argh <http://packages.python.org/argh/>`_
 * `opster <http://pypi.python.org/pypi/opster/>`_
 * `commandline <http://pypi.python.org/pypi/commandline>`_
 * `optfunc <https://github.com/simonw/optfunc>`_: this has the same concept
 * `commando (1) <http://freshmeat.net/projects/commando>`_
 * `commando (2) <https://github.com/lakshmivyas/commando>`_
 * argparse_
 * `optparse <http://docs.python.org/library/optparse.html>`_   
 * plumbum (https://github.com/tomerfiliba/plumbum)

Basic usage
============

Example::

	from entrypoint2 import entrypoint
	
	__version__ = '3.2'
	
	@entrypoint
	def add(one, two=4, three=False): 
	    ''' This function adds three numbers.
	    
	    one: first number to add
	    two: second number to add
	    '''

Generated help::

	$ python -m entrypoint2.examples.hello --help
	usage: hello.py [-h] [-t TWO] [--three] [--version] [--debug] one
	
	This function adds two number.
	
	positional arguments:
	  one                first number to add
	
	optional arguments:
	  -h, --help         show this help message and exit
	  -t TWO, --two TWO  second number to add
	  --three
	  --version          show program's version number and exit
	  --debug            set logging level to DEBUG

Printing version::

	$ python -m entrypoint2.examples.hello --version
	3.2


Installation
============

General:

 * install pip_
 * install the program::

    # as root
    pip install entrypoint2

Ubuntu::

    sudo apt-get install python-pip
    sudo pip install entrypoint2

Uninstall::

    # as root
    pip uninstall entrypoint2


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _entrypoint: http://pypi.python.org/pypi/entrypoint/
.. _autodoc: http://sphinx.pocoo.org/ext/autodoc.html
.. _argparse: http://docs.python.org/dev/library/argparse.html
