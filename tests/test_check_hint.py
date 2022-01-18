import sys

from easyprocess import EasyProcess

from entrypoint2 import PY39PLUS

python = sys.executable


def test_check_hints_int():
    if PY39PLUS:
        hints = """
list[str] -> list ['42']
list[bytes] -> list [b'42']
list[int] -> list [42]
list[float] -> list [42.0]
list[complex] -> list [(42+0j)]
list[bool] -> list [True]
    """.strip()
    else:
        hints = """
list[str] -> TypeError: 'type' object is not subscriptable
list[bytes] -> TypeError: 'type' object is not subscriptable
list[int] -> TypeError: 'type' object is not subscriptable
list[float] -> TypeError: 'type' object is not subscriptable
list[complex] -> TypeError: 'type' object is not subscriptable
list[bool] -> TypeError: 'type' object is not subscriptable
""".strip()

    hints += """
str -> str '42'
bytes -> bytes b'42'
int -> int 42
float -> float 42.0
complex -> complex (42+0j)
bool -> bool True
List[str] -> list ['42']
List[bytes] -> list [b'42']
List[int] -> list [42]
List[float] -> list [42.0]
List[complex] -> list [(42+0j)]
List[bool] -> list [True]
Sequence[str] -> list ['42']
Sequence[bytes] -> list [b'42']
Sequence[int] -> list [42]
Sequence[float] -> list [42.0]
Sequence[complex] -> list [(42+0j)]
Sequence[bool] -> list [True]
Iterable[str] -> list ['42']
Iterable[bytes] -> list [b'42']
Iterable[int] -> list [42]
Iterable[float] -> list [42.0]
Iterable[complex] -> list [(42+0j)]
Iterable[bool] -> list [True]
Optional[str] -> str '42'
Optional[bytes] -> bytes b'42'
Optional[int] -> int 42
Optional[float] -> float 42.0
Optional[complex] -> complex (42+0j)
Optional[bool] -> bool True
Any -> str '42'
"""
    p = EasyProcess([python, "-m", "entrypoint2.check.hints", "42"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == hints.strip().splitlines()


def test_check_hints_str():
    if PY39PLUS:
        hints = """
list[str] -> list ['abc']
list[bytes] -> list [b'abc']
list[int] -> -c: error: argument param: invalid int value: 'abc'
list[float] -> -c: error: argument param: invalid float value: 'abc'
list[complex] -> -c: error: argument param: invalid complex value: 'abc'
list[bool] -> list [True]
    """.strip()
    else:
        hints = """
list[str] -> TypeError: 'type' object is not subscriptable
list[bytes] -> TypeError: 'type' object is not subscriptable
list[int] -> TypeError: 'type' object is not subscriptable
list[float] -> TypeError: 'type' object is not subscriptable
list[complex] -> TypeError: 'type' object is not subscriptable
list[bool] -> TypeError: 'type' object is not subscriptable
""".strip()

    hints += """
str -> str 'abc'
bytes -> bytes b'abc'
int -> -c: error: argument param: invalid int value: 'abc'
float -> -c: error: argument param: invalid float value: 'abc'
complex -> -c: error: argument param: invalid complex value: 'abc'
bool -> bool True
List[str] -> list ['abc']
List[bytes] -> list [b'abc']
List[int] -> -c: error: argument param: invalid int value: 'abc'
List[float] -> -c: error: argument param: invalid float value: 'abc'
List[complex] -> -c: error: argument param: invalid complex value: 'abc'
List[bool] -> list [True]
Sequence[str] -> list ['abc']
Sequence[bytes] -> list [b'abc']
Sequence[int] -> -c: error: argument param: invalid int value: 'abc'
Sequence[float] -> -c: error: argument param: invalid float value: 'abc'
Sequence[complex] -> -c: error: argument param: invalid complex value: 'abc'
Sequence[bool] -> list [True]
Iterable[str] -> list ['abc']
Iterable[bytes] -> list [b'abc']
Iterable[int] -> -c: error: argument param: invalid int value: 'abc'
Iterable[float] -> -c: error: argument param: invalid float value: 'abc'
Iterable[complex] -> -c: error: argument param: invalid complex value: 'abc'
Iterable[bool] -> list [True]
Optional[str] -> str 'abc'
Optional[bytes] -> bytes b'abc'
Optional[int] -> -c: error: argument param: invalid int value: 'abc'
Optional[float] -> -c: error: argument param: invalid float value: 'abc'
Optional[complex] -> -c: error: argument param: invalid complex value: 'abc'
Optional[bool] -> bool True
Any -> str 'abc'
"""
    p = EasyProcess([python, "-m", "entrypoint2.check.hints", "abc"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == hints.strip().splitlines()


def test_check_hints_float():
    if PY39PLUS:
        hints = """
list[str] -> list ['42.1']
list[bytes] -> list [b'42.1']
list[int] -> -c: error: argument param: invalid int value: '42.1'
list[float] -> list [42.1]
list[complex] -> list [(42.1+0j)]
list[bool] -> list [True]
    """.strip()
    else:
        hints = """
list[str] -> TypeError: 'type' object is not subscriptable
list[bytes] -> TypeError: 'type' object is not subscriptable
list[int] -> TypeError: 'type' object is not subscriptable
list[float] -> TypeError: 'type' object is not subscriptable
list[complex] -> TypeError: 'type' object is not subscriptable
list[bool] -> TypeError: 'type' object is not subscriptable
""".strip()

    hints += """
str -> str '42.1'
bytes -> bytes b'42.1'
int -> -c: error: argument param: invalid int value: '42.1'
float -> float 42.1
complex -> complex (42.1+0j)
bool -> bool True
List[str] -> list ['42.1']
List[bytes] -> list [b'42.1']
List[int] -> -c: error: argument param: invalid int value: '42.1'
List[float] -> list [42.1]
List[complex] -> list [(42.1+0j)]
List[bool] -> list [True]
Sequence[str] -> list ['42.1']
Sequence[bytes] -> list [b'42.1']
Sequence[int] -> -c: error: argument param: invalid int value: '42.1'
Sequence[float] -> list [42.1]
Sequence[complex] -> list [(42.1+0j)]
Sequence[bool] -> list [True]
Iterable[str] -> list ['42.1']
Iterable[bytes] -> list [b'42.1']
Iterable[int] -> -c: error: argument param: invalid int value: '42.1'
Iterable[float] -> list [42.1]
Iterable[complex] -> list [(42.1+0j)]
Iterable[bool] -> list [True]
Optional[str] -> str '42.1'
Optional[bytes] -> bytes b'42.1'
Optional[int] -> -c: error: argument param: invalid int value: '42.1'
Optional[float] -> float 42.1
Optional[complex] -> complex (42.1+0j)
Optional[bool] -> bool True
Any -> str '42.1'
"""
    p = EasyProcess([python, "-m", "entrypoint2.check.hints", "42.1"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == hints.strip().splitlines()


def test_check_hints_0():
    if PY39PLUS:
        hints = """
list[str] -> list ['0']
list[bytes] -> list [b'0']
list[int] -> list [0]
list[float] -> list [0.0]
list[complex] -> list [0j]
list[bool] -> list [False]
    """.strip()
    else:
        hints = """
list[str] -> TypeError: 'type' object is not subscriptable
list[bytes] -> TypeError: 'type' object is not subscriptable
list[int] -> TypeError: 'type' object is not subscriptable
list[float] -> TypeError: 'type' object is not subscriptable
list[complex] -> TypeError: 'type' object is not subscriptable
list[bool] -> TypeError: 'type' object is not subscriptable
""".strip()

    hints += """
str -> str '0'
bytes -> bytes b'0'
int -> int 0
float -> float 0.0
complex -> complex 0j
bool -> bool False
List[str] -> list ['0']
List[bytes] -> list [b'0']
List[int] -> list [0]
List[float] -> list [0.0]
List[complex] -> list [0j]
List[bool] -> list [False]
Sequence[str] -> list ['0']
Sequence[bytes] -> list [b'0']
Sequence[int] -> list [0]
Sequence[float] -> list [0.0]
Sequence[complex] -> list [0j]
Sequence[bool] -> list [False]
Iterable[str] -> list ['0']
Iterable[bytes] -> list [b'0']
Iterable[int] -> list [0]
Iterable[float] -> list [0.0]
Iterable[complex] -> list [0j]
Iterable[bool] -> list [False]
Optional[str] -> str '0'
Optional[bytes] -> bytes b'0'
Optional[int] -> int 0
Optional[float] -> float 0.0
Optional[complex] -> complex 0j
Optional[bool] -> bool False
Any -> str '0'
"""
    p = EasyProcess([python, "-m", "entrypoint2.check.hints", "0"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == hints.strip().splitlines()


def test_check_hints_list_int():
    if PY39PLUS:
        hints = """
list[str] -> list ['3', '42']
list[bytes] -> list [b'3', b'42']
list[int] -> list [3, 42]
list[float] -> list [3.0, 42.0]
list[complex] -> list [(3+0j), (42+0j)]
list[bool] -> list [True, True]
    """.strip()
    else:
        hints = """
list[str] -> TypeError: 'type' object is not subscriptable
list[bytes] -> TypeError: 'type' object is not subscriptable
list[int] -> TypeError: 'type' object is not subscriptable
list[float] -> TypeError: 'type' object is not subscriptable
list[complex] -> TypeError: 'type' object is not subscriptable
list[bool] -> TypeError: 'type' object is not subscriptable
""".strip()

    hints += """
str -> -c: error: unrecognized arguments: 42
bytes -> -c: error: unrecognized arguments: 42
int -> -c: error: unrecognized arguments: 42
float -> -c: error: unrecognized arguments: 42
complex -> -c: error: unrecognized arguments: 42
bool -> -c: error: unrecognized arguments: 42
List[str] -> list ['3', '42']
List[bytes] -> list [b'3', b'42']
List[int] -> list [3, 42]
List[float] -> list [3.0, 42.0]
List[complex] -> list [(3+0j), (42+0j)]
List[bool] -> list [True, True]
Sequence[str] -> list ['3', '42']
Sequence[bytes] -> list [b'3', b'42']
Sequence[int] -> list [3, 42]
Sequence[float] -> list [3.0, 42.0]
Sequence[complex] -> list [(3+0j), (42+0j)]
Sequence[bool] -> list [True, True]
Iterable[str] -> list ['3', '42']
Iterable[bytes] -> list [b'3', b'42']
Iterable[int] -> list [3, 42]
Iterable[float] -> list [3.0, 42.0]
Iterable[complex] -> list [(3+0j), (42+0j)]
Iterable[bool] -> list [True, True]
Optional[str] -> -c: error: unrecognized arguments: 42
Optional[bytes] -> -c: error: unrecognized arguments: 42
Optional[int] -> -c: error: unrecognized arguments: 42
Optional[float] -> -c: error: unrecognized arguments: 42
Optional[complex] -> -c: error: unrecognized arguments: 42
Optional[bool] -> -c: error: unrecognized arguments: 42
Any -> -c: error: unrecognized arguments: 42
"""
    p = EasyProcess([python, "-m", "entrypoint2.check.hints", "3", "42"]).call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == hints.strip().splitlines()


def test_check_hints_bool():
    for par in ["0", "false", "False", "FALSE", "no"]:
        p = EasyProcess([python, "-m", "entrypoint2.check.hints", par]).call()
        assert p.stderr == ""
        assert p.return_code == 0
        assert "bool -> bool False" in p.stdout.splitlines()
    for par in ["1", "true", "True", "TRUE", "yes"]:
        p = EasyProcess([python, "-m", "entrypoint2.check.hints", par]).call()
        assert p.stderr == ""
        assert p.return_code == 0
        assert "bool -> bool True" in p.stdout.splitlines()
