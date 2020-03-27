import sys

from easyprocess import EasyProcess
from path import Path

python = sys.executable

d = Path(__file__).parent
example1_py = d / "example1.py"
example2_py = d / "example2.py"
example3_py = d / "example3.py"

PY3 = sys.version_info[0] >= 3


def ported_eq(a, b, msg=None):
    if not a == b:
        raise AssertionError(msg or "%r != %r" % (a, b))


def test_1_call():
    import example1

    ported_eq(example1.f(3), 3)
    ported_eq("description" in example1.f.__doc__, True)
    ported_eq(example1.f.__name__, "f")


def test_2_call():
    import example2

    ported_eq(example2.f(5, 1), 6)
    ported_eq(example2.f.__doc__, None)
    ported_eq(example2.f.__name__, "f")


def test_3_call():
    import example3

    ported_eq(example3.f(), 7)
    ported_eq(example3.f.__doc__, None)
    ported_eq(example3.f.__name__, "f")


def test_1_cli():
    cmd = [python, example1_py, "5"]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code, 0)
    ported_eq(p.stdout, "")
    ported_eq(p.stderr, "")

    cmd = [python, example1_py, "5", "--two", "7", "--debug"]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code, 0)
    ported_eq(p.stdout, "")
    ported_eq(p.stderr, "")

    cmd = [python, example1_py, "5", "--three", "-t", "2", "--debug"]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code, 0)
    ported_eq(p.stdout, "")
    ported_eq(p.stderr, "")

    cmd = [python, example1_py, "5", "-t", "x"]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code > 0, 1)
    ported_eq(p.stdout, "")
    ported_eq(p.stderr != "", 1)

    cmd = [python, example1_py, "-t", "1", "5", "--debug"]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code, 0)
    ported_eq(p.stdout, "")
    ported_eq(p.stderr, "")


def test_2_cli():
    cmd = [python, example2_py, "5", "2"]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code, 0)
    ported_eq(p.stdout, "")
    ported_eq(p.stderr, "")

    cmd = [python, example2_py, "--debug", "5", "2"]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code, 0)
    ported_eq(p.stdout, "")
    assert "root - DEBUG - 5" in p.stderr


def test_3_cli():
    cmd = [python, example3_py]
    p = EasyProcess(cmd).call()
    ported_eq(p.return_code, 0)
    ported_eq(p.stdout, "")
    ported_eq(p.stderr, "")


def test_1_ver():
    cmd = [python, example1_py, "--version"]
    p = EasyProcess(cmd).call()
    if PY3:
        ported_eq(p.stderr, "")
        ported_eq(p.stdout, "3.2")
    else:
        ported_eq(p.stdout, "")
        ported_eq(p.stderr, "3.2")
    ported_eq(p.return_code, 0)


def test_2_ver():
    cmd = [python, example2_py, "--version"]
    p = EasyProcess(cmd).call()
    if PY3:
        ported_eq(p.stderr, "")
        ported_eq(p.stdout, "1.2")
    else:
        ported_eq(p.stdout, "")
        ported_eq(p.stderr, "1.2")
    ported_eq(p.return_code, 0)


def test_3_ver():
    cmd = [python, example3_py, "--version"]
    p = EasyProcess(cmd).call()
    ported_eq(p.stdout, "")
    assert p.stderr
    assert p.return_code != 0


def test_1_help():
    cmd = [python, example1_py, "--help"]
    p = EasyProcess(cmd).call()
    ported_eq(p.stderr, "")
    ported_eq(p.return_code, 0)
    ported_eq("one" in p.stdout, 1)
    ported_eq("--two" in p.stdout, 1)
    ported_eq("-t" in p.stdout, 1)
    ported_eq("--three" in p.stdout, 1)


def test_2_help():
    cmd = [python, example2_py, "--help"]
    p = EasyProcess(cmd).call()
    ported_eq(p.stderr, "")
    ported_eq(p.return_code, 0)


def test_3_help():
    cmd = [python, example3_py, "--help"]
    p = EasyProcess(cmd).call()
    ported_eq(p.stderr, "")
    ported_eq(p.return_code, 0)
