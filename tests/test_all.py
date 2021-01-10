import os
import sys

from easyprocess import EasyProcess

python = sys.executable
join = os.path.join
d = os.path.dirname(__file__)
example1_py = join(d, "example1.py")
example2_py = join(d, "example2.py")
example3_py = join(d, "example3.py")


def test_1_call():
    import example1

    assert example1.f(3) == 3
    assert "description" in example1.f.__doc__
    assert example1.f.__name__ == "f"


def test_2_call():
    import example2

    assert example2.f(5, 1) == 6
    assert example2.f.__doc__ is None
    assert example2.f.__name__ == "f"


def test_3_call():
    import example3

    assert example3.f() == 7
    assert example3.f.__doc__ is None
    assert example3.f.__name__ == "f"


def test_1_cli():
    cmd = [python, example1_py, "5"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
    assert p.stderr == ""

    cmd = [python, example1_py, "5", "--two", "7", "--debug"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
    assert p.stderr == ""

    cmd = [python, example1_py, "5", "--three", "-t", "2", "--debug"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
    assert p.stderr == ""

    cmd = [python, example1_py, "5", "-t", "x"]
    p = EasyProcess(cmd).call()
    assert p.return_code > 0
    assert p.stdout == ""
    assert p.stderr != ""

    cmd = [python, example1_py, "-t", "1", "5", "--debug"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
    assert p.stderr == ""


def test_2_cli():
    cmd = [python, example2_py, "5", "2"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
    assert p.stderr == ""

    cmd = [python, example2_py, "--debug", "5", "2"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
    assert "root - DEBUG - 5" in p.stderr


def test_3_cli():
    cmd = [python, example3_py]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
    assert p.stderr == ""


def test_1_ver():
    cmd = [python, example1_py, "--version"]
    p = EasyProcess(cmd).call()
    assert p.stderr == ""
    assert p.stdout == "3.2"
    assert p.return_code == 0


def test_2_ver():
    cmd = [python, example2_py, "--version"]
    p = EasyProcess(cmd).call()
    assert p.stderr == ""
    assert p.stdout == "1.2"
    assert p.return_code == 0


def test_3_ver():
    cmd = [python, example3_py, "--version"]
    p = EasyProcess(cmd).call()
    assert p.stdout == ""
    assert p.stderr
    assert p.return_code != 0


def test_1_help():
    cmd = [python, example1_py, "--help"]
    p = EasyProcess(cmd).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert "one" in p.stdout
    assert "--two" in p.stdout
    assert "-t" in p.stdout
    assert "--three" in p.stdout


def test_2_help():
    cmd = [python, example2_py, "--help"]
    p = EasyProcess(cmd).call()
    assert p.stderr == ""
    assert p.return_code == 0


def test_3_help():
    cmd = [python, example3_py, "--help"]
    p = EasyProcess(cmd).call()
    assert p.stderr == ""
    assert p.return_code == 0
