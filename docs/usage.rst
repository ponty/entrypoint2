Usage
==================

Example program which adds 2 numbers:

.. literalinclude:: ../entrypoint2/examples/hello.py

Printing help with ``--help``:

.. program-output:: python -m entrypoint2.examples.hello --help
    :prompt:

Printing version with ``--version``:

.. program-output:: python -m entrypoint2.examples.hello --version
    :prompt:

Printing sum of two number by the program:

.. program-output:: python -m entrypoint2.examples.hello 3 --two 2
    :prompt:

The same but logging is activated:

.. program-output:: python -m entrypoint2.examples.hello 3 -t 2 --debug
    :prompt:

Example program which calls the adding function in previos module:

.. literalinclude:: ../entrypoint2/examples/caller.py

Calling without logging:

.. program-output:: python -m entrypoint2.examples.caller
    :prompt:

Calling with logging:

.. program-output:: python -m entrypoint2.examples.caller --debug
    :prompt:

    