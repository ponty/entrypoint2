import os
import sys

from easyprocess import EasyProcess

from entrypoint2 import entrypoint

python = sys.executable
join = os.path.join
d = os.path.dirname(__file__)

prog = """
from entrypoint2 import entrypoint
@entrypoint
def func(param={value}):
    print(type(param).__name__, repr(param))
    """


def run(value):
    cmd = [python, "-c", prog.format(value=value), "--debug", "--param"]
    if value not in ["False", "True"]:
        cmd += ["42"]
    p = EasyProcess(cmd).call()
    if p.return_code != 0 or p.stderr != "":
        raise ValueError(f"Error in Process call:{p}")
    return p.stdout


@entrypoint
def add():
    s = ""
    for x in [
        "None",
        "'str'",
        "b'bytes'",
        "1",
        "1.1",
        "[]",
        "None",
        "False",
        "True",
    ]:
        s = "{} -> {}".format(x, run(x))
        print(s)
