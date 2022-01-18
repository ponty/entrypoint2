import os
import sys

from easyprocess import EasyProcess

python = sys.executable
join = os.path.join
d = os.path.dirname(__file__)
example_py = join(d, "example_typehint.py")


def run(py, params, stdout=""):
    cmd = [python, "-c", py] + params
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == stdout
    assert p.stderr == ""


def test_type_str():
    run(
        """
from entrypoint2 import entrypoint
@entrypoint
def flen(x: str):
    assert type(x) == str
    """,
        ["42"],
    )


def test_type_int():
    run(
        """
from entrypoint2 import entrypoint
@entrypoint
def flen(x: int):
    assert type(x) == int, repr(x)
    """,
        ["42"],
    )


def test_call():
    import example_typehint as ex

    assert ex.flen("33", None, 1, 0.1, True) == 6.1
    assert "12345" == ex.flen.__doc__
    assert ex.flen.__name__ == "flen"
