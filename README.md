entrypoint2 is an easy to use [argparse][2] based command-line interface for python modules.
It translates function signature and documentation to [argparse][2] configuration.


Links:

 * home: https://github.com/ponty/entrypoint2
 * PYPI: https://pypi.python.org/pypi/entrypoint2

[![Build Status](https://travis-ci.org/ponty/entrypoint2.svg?branch=master)](https://travis-ci.org/ponty/entrypoint2)

Goals:

 - simplicity: only one decorator to add to existing code

Features:

 - good for protoyping or simple CLI
 - generate CLI parameters from function signature 
 - generate CLI documentation from python documentation 
 - the decorated function has the same behavior as without the entrypoint2 decorator
 - boolean parameters are toggle flags (e.g. ``--verbose``) 
 - function signature is preserved so it can be called both from command-line and external module
 - function name, doc and module are preserved so it can be used with sphinx [autodoc][1]
 - sphinx [autodoc][1] documentation style is supported: ``:param x: this is x``
 - automatic ``--version`` flag, which prints version variable from the current module
   (``__version__``, ``VERSION``, ..) 
 - automatic ``--debug`` flag, which turns on logging 
 - short flags are generated from long flags automatically (e.g. ``--parameter`` -> ``-p``) 
 - supported python versions: 3.6, 3.7, 3.8, 3.9
 - support for repeating arguments

installation:

```console
$ python3 -m pip install entrypoint2
```

Basic usage
============

Example:

```py
# entrypoint2/examples/hello.py

import logging

from entrypoint2 import entrypoint

__version__ = "3.2"


@entrypoint
def add(one, two=4, three=False):
    """ This function adds two numbers.

    :param one: first number to add
    :param two: second number to add
    :param three: print hello
    :rtype: int
    """
    s = int(one) + int(two)
    logging.debug(s)
    print(s)
    if three:
        print("hello")
    return s

```

Adding numbers:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_1.txt -->

```console
$ python3 -m entrypoint2.examples.hello 1
5
```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_1_--two_1.txt -->

```console
$ python3 -m entrypoint2.examples.hello 1 --two 1
2
```

Short flag:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_1_-t_1.txt -->

```console
$ python3 -m entrypoint2.examples.hello 1 -t 1
2
```

Boolean parameter:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_1_--three.txt -->

```console
$ python3 -m entrypoint2.examples.hello 1 --three
5
hello
```

Logging:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_1_--debug.txt -->

```console
$ python3 -m entrypoint2.examples.hello 1 --debug
2020-10-01 07:41:17,197: root - DEBUG - 5
5
```

Missing positional parameter:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello.txt -->

```console
$ python3 -m entrypoint2.examples.hello
usage: hello.py [-h] [-t TWO] [--three] [--debug] [--version] one
hello.py: error: the following arguments are required: one
```

Generated help:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_--help.txt -->

```console
$ python3 -m entrypoint2.examples.hello --help
usage: hello.py [-h] [-t TWO] [--three] [--debug] [--version] one

This function adds two numbers.

positional arguments:
  one                first number to add

optional arguments:
  -h, --help         show this help message and exit
  -t TWO, --two TWO  second number to add
  --three            print hello
  --debug            set logging level to DEBUG
  --version          show program's version number and exit
```

Printing version:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_--version.txt -->

```console
$ python3 -m entrypoint2.examples.hello --version
3.2
```

Repeating arguments
===================

Example:

```py
# entrypoint2/examples/repeating.py

from entrypoint2 import entrypoint


@entrypoint
def main(files=[]):
    """ This function has repeating arguments.
    :param files: test input
    """
    print(files)

```

Only string list is supported 
  

Printing help:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.repeating_--help.txt -->

```console
$ python3 -m entrypoint2.examples.repeating --help
usage: repeating.py [-h] [-f FILES] [--debug]

This function has repeating arguments.

optional arguments:
  -h, --help            show this help message and exit
  -f FILES, --files FILES
                        test input
  --debug               set logging level to DEBUG
```

Repeating flag:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.repeating_-f_input1.txt_-f_input2.txt.txt -->

```console
$ python3 -m entrypoint2.examples.repeating -f input1.txt -f input2.txt
['input1.txt', 'input2.txt']
```


[1]: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
[2]: http://docs.python.org/dev/library/argparse.html


