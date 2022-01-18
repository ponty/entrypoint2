import sys

from easyprocess import EasyProcess

python = sys.executable


def test_check_defaults_int():
    defaults = """
None -> str '42'
'str' -> str '42'
b'bytes' -> bytes b'42'
[] -> list ['42']
1 -> int 42
1.1 -> float 42.0
False -> -c: error: unrecognized arguments: 42
True -> -c: error: unrecognized arguments: 42
    """.strip().splitlines()
    p = EasyProcess([python, "-m", "entrypoint2.check.defaults", "42"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == defaults


def test_check_defaults_str():
    defaults = """
None -> str 'abc'
'str' -> str 'abc'
b'bytes' -> bytes b'abc'
[] -> list ['abc']
1 -> -c: error: argument -p/--param: invalid int value: 'abc'
1.1 -> -c: error: argument -p/--param: invalid float value: 'abc'
False -> -c: error: unrecognized arguments: abc
True -> -c: error: unrecognized arguments: abc
    """.strip().splitlines()
    p = EasyProcess([python, "-m", "entrypoint2.check.defaults", "abc"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == defaults


def test_check_defaults_float():
    defaults = """
None -> str '21.3'
'str' -> str '21.3'
b'bytes' -> bytes b'21.3'
[] -> list ['21.3']
1 -> -c: error: argument -p/--param: invalid int value: '21.3'
1.1 -> float 21.3
False -> -c: error: unrecognized arguments: 21.3
True -> -c: error: unrecognized arguments: 21.3
    """.strip().splitlines()
    p = EasyProcess([python, "-m", "entrypoint2.check.defaults", "21.3"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == defaults


def test_check_defaults_noval():
    defaults = """
None -> -c: error: argument -p/--param: expected one argument
'str' -> -c: error: argument -p/--param: expected one argument
b'bytes' -> -c: error: argument -p/--param: expected one argument
[] -> -c: error: argument -p/--param: expected one argument
1 -> -c: error: argument -p/--param: expected one argument
1.1 -> -c: error: argument -p/--param: expected one argument
False -> bool True
True -> bool False
    """.strip().splitlines()
    p = EasyProcess([python, "-m", "entrypoint2.check.defaults", "noval"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == defaults


def test_check_defaults_nopar():
    defaults = """
None -> NoneType None
'str' -> str 'str'
b'bytes' -> bytes b'bytes'
[] -> list []
1 -> int 1
1.1 -> float 1.1
False -> bool False
True -> bool True
    """.strip().splitlines()
    p = EasyProcess([python, "-m", "entrypoint2.check.defaults", "nopar"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == defaults


def test_check_defaults_repeat():
    defaults = """
None -> str '3'
'str' -> str '3'
b'bytes' -> bytes b'3'
[] -> list ['1', '2', '3']
1 -> int 3
1.1 -> float 3.0
False -> -c: error: unrecognized arguments: 1 2 3
True -> -c: error: unrecognized arguments: 1 2 3
    """.strip().splitlines()
    p = EasyProcess([python, "-m", "entrypoint2.check.defaults", "1,2,3"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == defaults
