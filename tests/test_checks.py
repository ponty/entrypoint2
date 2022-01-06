from easyprocess import EasyProcess

defaults = """
None -> str '42'
'str' -> str '42'
b'bytes' -> bytes b'42'
1 -> int 42
1.1 -> float 42.0
[] -> list ['42']
None -> str '42'
False -> bool True
True -> bool False
""".strip().splitlines()

hints = """
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
""".strip().splitlines()


def test_check_defaults():
    p = EasyProcess("python3 -m entrypoint2.check.defaults").call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == defaults


def test_check_hints():
    p = EasyProcess("python3 -m entrypoint2.check.hints").call()
    assert p.stderr == ""
    assert p.return_code == 0
    assert p.stdout.splitlines() == hints
