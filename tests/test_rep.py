import sys

from easyprocess import EasyProcess

from entrypoint2 import PY39PLUS

python = sys.executable


def run(py, params, stdout=""):
    cmd = [python, "-c", py] + params
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == stdout
    assert p.stderr == ""


def test_def():
    prog_list = """
from entrypoint2 import entrypoint
@entrypoint
def f(x=[]):
    print(x)
        """
    run(
        prog_list,
        ["--x", "42"],
        "['42']",
    )
    run(
        prog_list,
        ["--x", "42", "--x", "43"],
        "['42', '43']",
    )
    run(
        prog_list,
        [],
        "[]",
    )


if PY39PLUS:

    def test_1():
        prog_list = """
from entrypoint2 import entrypoint
@entrypoint
def f(x: list[int]):
    print(x)
        """
        run(
            prog_list,
            ["42"],
            "[42]",
        )
        run(
            prog_list,
            ["42", "43"],
            "[42, 43]",
        )
        run(
            prog_list,
            [],
            "[]",
        )

    def test_2():
        prog_list = """
from entrypoint2 import entrypoint
@entrypoint
def f(a:int, x: list[int]):
    print(a, x)
        """
        run(
            prog_list,
            ["42"],
            "42 []",
        )
        run(
            prog_list,
            ["42", "43", "44"],
            "42 [43, 44]",
        )

    def test_3():
        prog_list = """
from entrypoint2 import entrypoint
@entrypoint
def f(x: list[int], a:int):
    print(x, a)
        """
        run(
            prog_list,
            ["42"],
            "[] 42",
        )
        run(
            prog_list,
            ["42", "43", "44"],
            "[42, 43] 44",
        )
