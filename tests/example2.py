import logging

from entrypoint2 import entrypoint

VERSION = "1.2"


@entrypoint
def f(x, y):
    logging.debug(x)
    return x + y
