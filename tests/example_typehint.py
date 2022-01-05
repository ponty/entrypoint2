from typing import Optional

from entrypoint2 import entrypoint

# no VERSION


@entrypoint
def flen(s: str, opt: Optional[int], i: int, f: float, add3: bool):
    "12345"
    x = 0.0
    x += len(s)
    if opt is not None:
        x += opt
    if i:
        x += i
    if f:
        x += f
    if add3:
        x += 3
    print(x)
    return x
