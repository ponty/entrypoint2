entrypoint2 is an easy to use [argparse][2] based command-line interface for python modules.
It translates function signature and documentation to [argparse][2] configuration.


Links:

 * home: https://github.com/ponty/entrypoint2
 * PYPI: https://pypi.python.org/pypi/entrypoint2

![workflow](https://github.com/ponty/entrypoint2/actions/workflows/main.yml/badge.svg)

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
 - supported python versions: 3.6, 3.7, 3.8, 3.9, 3.10
 - support for repeating arguments

installation:

```console
$ python3 -m pip install entrypoint2
```

Hello world
===========

```py
# entrypoint2/examples/hello.py

from entrypoint2 import entrypoint


@entrypoint
def hello(message):
    # type of 'message' is not defined, default is str
    print(message)

```

Generated help:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_--help.txt -->

```console
$ python3 -m entrypoint2.examples.hello --help
usage: hello.py [-h] [--debug] message

positional arguments:
  message

options:
  -h, --help  show this help message and exit
  --debug     set logging level to DEBUG
```

Running:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.hello_hi.txt -->

```console
$ python3 -m entrypoint2.examples.hello hi
hi
```

Basic usage
============

Example:

```py
# entrypoint2/examples/add.py

import logging

from entrypoint2 import entrypoint

__version__ = "3.2"


@entrypoint
def add(one: int, two=4, three=False):
    """This function adds two numbers.

    :param one: first number to add
    :param two: second number to add
    :param three: print hello if True
    :rtype: int
    """

    # 'one' and 'two' are converted to int
    s = one + two

    logging.debug(s)
    print(s)
    if three:
        print("hello")
    return s

```

Generated help:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.add_--help.txt -->

```console
$ python3 -m entrypoint2.examples.add --help
usage: add.py [-h] [-t TWO] [--three] [--debug] [--version] one

This function adds two numbers.

positional arguments:
  one                first number to add

options:
  -h, --help         show this help message and exit
  -t TWO, --two TWO  second number to add
  --three            print hello if True
  --debug            set logging level to DEBUG
  --version          show program's version number and exit
```

Positional parameter:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.add_1.txt -->

```console
$ python3 -m entrypoint2.examples.add 1
5
```

Optional parameter:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.add_1_--two_1.txt -->

```console
$ python3 -m entrypoint2.examples.add 1 --two 1
2
```

Short flag:
First parameter with first letter 't' is used ('two'). 
Next parameters with same first letter ('three') has no short flag.
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.add_1_-t_1.txt -->

```console
$ python3 -m entrypoint2.examples.add 1 -t 1
2
```

Boolean parameter:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.add_1_--three.txt -->

```console
$ python3 -m entrypoint2.examples.add 1 --three
5
hello
```

Logging:

`--debug` is a special flag, it sets logging level to DEBUG with this call:
```py
logging.basicConfig(level=logging.DEBUG, format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
```

Logging example:

```console
$ python3 -m entrypoint2.examples.add 1 --debug
2021-04-05 13:30:15,590: root - DEBUG - 5
5
```

Missing positional parameter:
<!-- embedme doc/gen/python3_-m_entrypoint2.examples.add.txt -->

```console
$ python3 -m entrypoint2.examples.add
usage: add.py [-h] [-t TWO] [--three] [--debug] [--version] one
add.py: error: the following arguments are required: one
```

Printing version:

`--version` is a special flag, it prints the program's version number and exit.
The version can be set with one of this line:
```py
__version__ = "1.0"
VERSION = "1.0" 
version = "1.0"
```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.add_--version.txt -->

```console
$ python3 -m entrypoint2.examples.add --version
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
    """This function has repeating arguments.
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

options:
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

type hints
==========

The parameter conversion is based on the type hint. 
If the hint is 'int' then the command line parameter is converted from string to int.

```py
# entrypoint2/examples/typehints.py

from entrypoint2 import entrypoint


@entrypoint
def func(
    strpar: str,
    bytespar: bytes,
    intpar: int,
    floatpar: float,
    boolpar: bool,
    listpar: list[int],
):
    print(f"strpar={repr(strpar)}")
    print(f"bytespar={repr(bytespar)}")
    print(f"intpar={repr(intpar)}")
    print(f"floatpar={repr(floatpar)}")
    print(f"boolpar={repr(boolpar)}")
    print(f"listpar={repr(listpar)}")

```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.typehints_-h.txt -->

```console
$ python3 -m entrypoint2.examples.typehints -h
usage: typehints.py [-h] [--debug]
                    strpar bytespar intpar floatpar boolpar [listpar ...]

positional arguments:
  strpar
  bytespar
  intpar
  floatpar
  boolpar
  listpar

options:
  -h, --help  show this help message and exit
  --debug     set logging level to DEBUG
```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.typehints_1_2_3_4_5_6_7.txt -->

```console
$ python3 -m entrypoint2.examples.typehints 1 2 3 4 5 6 7
strpar='1'
bytespar=b'2'
intpar=3
floatpar=4.0
boolpar=True
listpar=[6, 7]
```


default value
=============

The parameter conversion is based on the default value. 
If the default value is an int value like '21' then the command line parameter is converted from string to int.

```py
# entrypoint2/examples/defaultvalues.py

from entrypoint2 import entrypoint


@entrypoint
def add(
    strpar="string",
    bytespar=b"bytes",
    intpar=21,
    floatpar=3.14,
    boolpar=False,
):
    print(f"strpar={repr(strpar)}")
    print(f"bytespar={repr(bytespar)}")
    print(f"intpar={repr(intpar)}")
    print(f"floatpar={repr(floatpar)}")
    print(f"boolpar={repr(boolpar)}")

```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.defaultvalues_-h.txt -->

```console
$ python3 -m entrypoint2.examples.defaultvalues -h
usage: defaultvalues.py [-h] [-s STRPAR] [-b BYTESPAR] [-i INTPAR]
                        [-f FLOATPAR] [--boolpar] [--debug]

options:
  -h, --help            show this help message and exit
  -s STRPAR, --strpar STRPAR
  -b BYTESPAR, --bytespar BYTESPAR
  -i INTPAR, --intpar INTPAR
  -f FLOATPAR, --floatpar FLOATPAR
  --boolpar
  --debug               set logging level to DEBUG
```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.defaultvalues_-s_1_-b_1_-i_1_-f_1_--boolpar.txt -->

```console
$ python3 -m entrypoint2.examples.defaultvalues -s 1 -b 1 -i 1 -f 1 --boolpar
strpar='1'
bytespar=b'1'
intpar=1
floatpar=1.0
boolpar=True
```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.defaultvalues_-s_hello_-b_hello_-i_3_-f_3.141.txt -->

```console
$ python3 -m entrypoint2.examples.defaultvalues -s hello -b hello -i 3 -f 3.141
strpar='hello'
bytespar=b'hello'
intpar=3
floatpar=3.141
boolpar=False
```

Variable-length arguments (varargs)
===================================


```py
# entrypoint2/examples/varargs.py

from entrypoint2 import entrypoint


@entrypoint
def func(*args):
    print(args)

```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.varargs_-h.txt -->

```console
$ python3 -m entrypoint2.examples.varargs -h
usage: varargs.py [-h] [--debug] [args ...]

positional arguments:
  args

options:
  -h, --help  show this help message and exit
  --debug     set logging level to DEBUG
```

<!-- embedme doc/gen/python3_-m_entrypoint2.examples.varargs_a_b_c.txt -->

```console
$ python3 -m entrypoint2.examples.varargs a b c
('a', 'b', 'c')
```


[1]: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
[2]: http://docs.python.org/dev/library/argparse.html


