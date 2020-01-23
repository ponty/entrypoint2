from entrypoint2 import entrypoint

__version__ = "3.2"

# 'hi': test conflict with -h (--help)


@entrypoint
def f(one, two=4, three=False, hi=7):
    """ description

    one: par1
    two: par2
    """
    return one
