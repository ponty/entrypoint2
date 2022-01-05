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


# def test_type_float():
#     run(
#         """
# from entrypoint2 import entrypoint
# @entrypoint
# def flen(x: float):
#     assert type(x) == float
#     """,
#         ["42"],
#     )


# def test_type_opt_str():
#     run(
#         """
# from entrypoint2 import entrypoint
# from typing import Optional
# @entrypoint
# def flen(x: Optional[str]):
#     assert x is None
#     """,
#         [],
#     )
#     run(
#         """
# from entrypoint2 import entrypoint
# from typing import Optional
# @entrypoint
# def flen(x: Optional[str]):
#     assert type(x) == str
#     """,
#         ['--x',"42"],
#     )


def test_call():
    import example_typehint as ex

    assert ex.flen("33", None, 1, 0.1, True) == 6.1
    assert "12345" == ex.flen.__doc__
    assert ex.flen.__name__ == "flen"


# def test_1_cli():
#     cmd = [python, example_py, "33", "0", "1", "0.1", "1"]
#     p = EasyProcess(cmd).call()
#     assert p.return_code == 6.1
#     assert p.stdout == ""
#     assert p.stderr == ""


#     cmd = [python, example_py, "5", "--two", "7", "--debug"]
#     p = EasyProcess(cmd).call()
#     assert p.return_code == 0
#     assert p.stdout == ""
#     assert p.stderr == ""

#     cmd = [python, example_py, "5", "--three", "-t", "2", "--debug"]
#     p = EasyProcess(cmd).call()
#     assert p.return_code == 0
#     assert p.stdout == ""
#     assert p.stderr == ""

#     cmd = [python, example_py, "5", "-t", "x"]
#     p = EasyProcess(cmd).call()
#     assert p.return_code > 0
#     assert p.stdout == ""
#     assert p.stderr != ""

#     cmd = [python, example_py, "-t", "1", "5", "--debug"]
#     p = EasyProcess(cmd).call()
#     assert p.return_code == 0
#     assert p.stdout == ""
#     assert p.stderr == ""


# def test_2_cli():
#     cmd = [python, example2_py, "5", "2"]
#     p = EasyProcess(cmd).call()
#     assert p.return_code == 0
#     assert p.stdout == ""
#     assert p.stderr == ""

#     cmd = [python, example2_py, "--debug", "5", "2"]
#     p = EasyProcess(cmd).call()
#     assert p.return_code == 0
#     assert p.stdout == ""
#     assert "root - DEBUG - 5" in p.stderr


# def test_3_cli():
#     cmd = [python, example3_py]
#     p = EasyProcess(cmd).call()
#     assert p.return_code == 0
#     assert p.stdout == ""
#     assert p.stderr == ""


# def test_1_ver():
#     cmd = [python, example_py, "--version"]
#     p = EasyProcess(cmd).call()
#     assert p.stderr == ""
#     assert p.stdout == "3.2"
#     assert p.return_code == 0


# def test_2_ver():
#     cmd = [python, example2_py, "--version"]
#     p = EasyProcess(cmd).call()
#     assert p.stderr == ""
#     assert p.stdout == "1.2"
#     assert p.return_code == 0


# def test_3_ver():
#     cmd = [python, example3_py, "--version"]
#     p = EasyProcess(cmd).call()
#     assert p.stdout == ""
#     assert p.stderr
#     assert p.return_code != 0


# def test_1_help():
#     cmd = [python, example_py, "--help"]
#     p = EasyProcess(cmd).call()
#     assert p.stderr == ""
#     assert p.return_code == 0
#     assert "one" in p.stdout
#     assert "--two" in p.stdout
#     assert "-t" in p.stdout
#     assert "--three" in p.stdout


# def test_2_help():
#     cmd = [python, example2_py, "--help"]
#     p = EasyProcess(cmd).call()
#     assert p.stderr == ""
#     assert p.return_code == 0


# def test_3_help():
#     cmd = [python, example3_py, "--help"]
#     p = EasyProcess(cmd).call()
#     assert p.stderr == ""
#     assert p.return_code == 0
