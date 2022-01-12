import glob
import logging
import os

from easyprocess import EasyProcess

from entrypoint2 import entrypoint

commands = [
    "python3 -m entrypoint2.examples.hello --help",
    "python3 -m entrypoint2.examples.hello hi",
    "python3 -m entrypoint2.examples.add 1",
    "python3 -m entrypoint2.examples.add 1 --two 1",
    "python3 -m entrypoint2.examples.add 1 -t 1",
    "python3 -m entrypoint2.examples.add 1 --three",
    "python3 -m entrypoint2.examples.add",
    "python3 -m entrypoint2.examples.add --help",
    "python3 -m entrypoint2.examples.add --version",
    "python3 -m entrypoint2.examples.repeating --help",
    "python3 -m entrypoint2.examples.repeating -f input1.txt -f input2.txt",
    "python3 -m entrypoint2.examples.typehints -h",
    "python3 -m entrypoint2.examples.typehints 0 0 0 0 0",
    "python3 -m entrypoint2.examples.typehints 1 1 1 1 1",
    "python3 -m entrypoint2.examples.defaultvalues -h",
    "python3 -m entrypoint2.examples.defaultvalues -s 1 -b 1 -i 1 -f 1 --boolpar",
    "python3 -m entrypoint2.examples.defaultvalues -s hello -b hello -i 3 -f 3.141",
    "python3 -m entrypoint2.examples.varargs -h",
    "python3 -m entrypoint2.examples.varargs a b c",
]
# "python3 -m entrypoint2.examples.add 1 --debug",


def empty_dir(dir):
    files = glob.glob(os.path.join(dir, "*"))
    for f in files:
        os.remove(f)


@entrypoint
def main():
    gendir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen")
    logging.info("gendir: %s", gendir)
    os.makedirs(gendir, exist_ok=True)
    empty_dir(gendir)
    try:
        os.chdir("gen")
        for cmd in commands:
            logging.info("cmd: %s", cmd)
            fname_base = cmd.replace(" ", "_")
            fname = fname_base + ".txt"
            logging.info("cmd: %s", cmd)
            print("file name: %s" % fname)
            with open(fname, "w") as f:
                f.write("$ " + cmd + "\n")
                p = EasyProcess(cmd).call()
                f.write(p.stderr)
                if p.stderr and p.stdout:
                    f.write("\n")
                f.write(p.stdout)
    finally:
        os.chdir("..")
    embedme = EasyProcess(["npx", "embedme", "../README.md"])
    embedme.call()
    print(embedme.stdout)
    assert embedme.return_code == 0
    assert not "but file does not exist" in embedme.stdout
