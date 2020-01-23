import sys

from easyprocess import EasyProcess
from nose.tools import eq_, ok_
from path import Path

python = sys.executable

d = Path(__file__).parent
example1_py = d / "example1.py"
example2_py = d / "example2.py"
example3_py = d / "example3.py"

PY3 = sys.version_info[0] >= 3


def test_1_call():
    import example1

    eq_(example1.f(3), 3)
    eq_("description" in example1.f.__doc__, True)
    eq_(example1.f.__name__, "f")


def test_2_call():
    import example2

    eq_(example2.f(5, 1), 6)
    eq_(example2.f.__doc__, None)
    eq_(example2.f.__name__, "f")


def test_3_call():
    import example3

    eq_(example3.f(), 7)
    eq_(example3.f.__doc__, None)
    eq_(example3.f.__name__, "f")


def test_1_cli():
    cmd = [python, example1_py, "5"]
    p = EasyProcess(cmd).call()
    eq_(p.return_code, 0)
    eq_(p.stdout, "")
    eq_(p.stderr, "")

    cmd = [python, example1_py, "5", "--two", "7", "--debug"]
    p = EasyProcess(cmd).call()
    eq_(p.return_code, 0)
    eq_(p.stdout, "")
    eq_(p.stderr, "")

    cmd = [python, example1_py, "5", "--three", "-t", "2", "--debug"]
    p = EasyProcess(cmd).call()
    eq_(p.return_code, 0)
    eq_(p.stdout, "")
    eq_(p.stderr, "")

    cmd = [python, example1_py, "5", "-t", "x"]
    p = EasyProcess(cmd).call()
    eq_(p.return_code > 0, 1)
    eq_(p.stdout, "")
    eq_(p.stderr != "", 1)

    cmd = [python, example1_py, "-t", "1", "5", "--debug"]
    p = EasyProcess(cmd).call()
    eq_(p.return_code, 0)
    eq_(p.stdout, "")
    eq_(p.stderr, "")


def test_2_cli():
    cmd = [python, example2_py, "5", "2"]
    p = EasyProcess(cmd).call()
    eq_(p.return_code, 0)
    eq_(p.stdout, "")
    eq_(p.stderr, "")

    cmd = [python, example2_py, "--debug", "5", "2"]
    p = EasyProcess(cmd).call()
    eq_(p.return_code, 0)
    eq_(p.stdout, "")
    ok_("root - DEBUG - 5" in p.stderr)


def test_3_cli():
    cmd = [python, example3_py]
    p = EasyProcess(cmd).call()
    eq_(p.return_code, 0)
    eq_(p.stdout, "")
    eq_(p.stderr, "")


def test_1_ver():
    cmd = [python, example1_py, "--version"]
    p = EasyProcess(cmd).call()
    if PY3:
        eq_(p.stderr, "")
        eq_(p.stdout, "3.2")
    else:
        eq_(p.stdout, "")
        eq_(p.stderr, "3.2")
    eq_(p.return_code, 0)


def test_2_ver():
    cmd = [python, example2_py, "--version"]
    p = EasyProcess(cmd).call()
    if PY3:
        eq_(p.stderr, "")
        eq_(p.stdout, "1.2")
    else:
        eq_(p.stdout, "")
        eq_(p.stderr, "1.2")
    eq_(p.return_code, 0)


def test_3_ver():
    cmd = [python, example3_py, "--version"]
    p = EasyProcess(cmd).call()
    eq_(p.stdout, "")
    ok_(p.stderr)
    ok_(p.return_code != 0)


def test_1_help():
    cmd = [python, example1_py, "--help"]
    p = EasyProcess(cmd).call()
    eq_(p.stderr, "")
    eq_(p.return_code, 0)
    eq_("one" in p.stdout, 1)
    eq_("--two" in p.stdout, 1)
    eq_("-t" in p.stdout, 1)
    eq_("--three" in p.stdout, 1)


def test_2_help():
    cmd = [python, example2_py, "--help"]
    p = EasyProcess(cmd).call()
    eq_(p.stderr, "")
    eq_(p.return_code, 0)


def test_3_help():
    cmd = [python, example3_py, "--help"]
    p = EasyProcess(cmd).call()
    eq_(p.stderr, "")
    eq_(p.return_code, 0)
