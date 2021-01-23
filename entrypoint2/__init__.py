import argparse
import inspect
import logging
import re
import sys
import textwrap


def _module_version(func):
    version = None
    for v in "__version__ VERSION version".split():
        version = func.__globals__.get(v)
        if version:
            break
    return version


class _ParagraphPreservingArgParseFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super(_ParagraphPreservingArgParseFormatter, self).__init__(*args, **kwargs)
        self._long_break_matcher = argparse._re.compile(r"\n\n+")

    def _fill_text(self, text, width, indent):
        output = []
        for block in self._long_break_matcher.split(text.strip()):
            output.append(
                textwrap.fill(
                    block, width, initial_indent=indent, subsequent_indent=indent
                )
            )
        return "\n\n".join(output + [""])


def _parse_doc(docs):
    # Converts a well-formed docstring into documentation
    # to be fed into argparse.

    # See signature_parser for details.

    # shorts: (-k for --keyword -k, or "from" for "frm/from")
    # metavars: (FILE for --input=FILE)
    # helps: (docs for --keyword: docs)
    # description: the stuff before
    # epilog: the stuff after

    name = "(?:[a-zA-Z][a-zA-Z0-9-_]*)"

    re_var = re.compile(r"^ *(%s)(?: */(%s))? *:(.*)$" % (name, name))
    re_opt = re.compile(
        r"^ *(?:(-[a-zA-Z0-9]),? +)?--(%s)(?: *=(%s))? *:(.*)$" % (name, name)
    )

    shorts, metavars, helps, description, epilog = {}, {}, {}, "", ""

    if docs:

        for line in docs.split("\n"):

            line = line.strip()

            # remove starting ':param'
            if line.startswith(":param"):
                line = line[len(":param") :]

            # skip ':rtype:' row
            if line.startswith(":rtype:"):
                continue

            if line.strip() == "----":
                break

            m = re_var.match(line)
            if m:
                if epilog:
                    helps[prev] += epilog.strip()
                    epilog = ""

                if m.group(2):
                    shorts[m.group(1)] = m.group(2)

                helps[m.group(1)] = m.group(3).strip()
                prev = m.group(1)
                previndent = len(line) - len(line.lstrip())
                continue

            m = re_opt.match(line)
            if m:
                if epilog:
                    helps[prev] += epilog.strip()
                    epilog = ""
                name = m.group(2).replace("-", "_")
                helps[name] = m.group(4)
                prev = name

                if m.group(1):
                    shorts[name] = m.group(1)
                if m.group(3):
                    metavars[name] = m.group(3)

                previndent = len(line) - len(line.lstrip())
                continue

            if helps:
                if line.startswith(" " * (previndent + 1)):
                    helps[prev] += "\n" + line.strip()
                else:
                    epilog += "\n" + line.strip()
            else:
                description += "\n" + line.strip()

            if line.strip():
                previndent = len(line) - len(line.lstrip())

    return shorts, metavars, helps, description, epilog


def _signature_parser(func):
    # args, varargs, varkw, defaults = inspect.getargspec(func)
    (
        args,
        varargs,
        varkw,
        defaults,
        kwonlyargs,
        kwonlydefaults,
        annotations,
    ) = inspect.getfullargspec(func)

    if not args:
        args = []

    if not defaults:
        defaults = []

    if varkw:
        raise Exception("Can't wrap a function with **kwargs")

    # Compulsary positional options
    needed = args[0 : len(args) - len(defaults)]

    # Optional flag options
    params = args[len(needed) :]

    shorts, metavars, helps, description, epilog = _parse_doc(func.__doc__)

    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=_ParagraphPreservingArgParseFormatter,
    )

    # special flags
    special_flags = []

    special_flags += ["debug"]
    defaults += (False,)
    helps["debug"] = "set logging level to DEBUG"
    if _module_version(func):
        special_flags += ["version"]
        defaults += (False,)
        helps["version"] = "show program's version number and exit"
    params += special_flags

    # Optional flag options
    used_shorts = set()
    for param, default in zip(params, defaults):
        args = ["--%s" % param.replace("_", "-")]
        short = None
        if param in shorts:
            short = shorts[param]
        else:
            if param not in special_flags and len(param) > 1:
                first_char = param[0]
                if first_char not in used_shorts:
                    used_shorts.add(first_char)
                    short = "-" + first_char
        # -h conflicts with 'help'
        if short and short != "-h":
            args = [short] + args

        d = {"default": default, "dest": param.replace("-", "_")}

        if param == "version":
            d["action"] = "version"
            d["version"] = _module_version(func)
        elif default is True:
            d["action"] = "store_false"
        elif default is False:
            d["action"] = "store_true"
        elif isinstance(default, list):
            d["action"] = "append"
            #  default is not working
            #            if len(default):
            #                first = default[0]
            #                if type(first) in [type(None), unicode]:
            #                    kwargs['type'] = lambda x: x
            #                else:
            #                    kwargs['type'] = type(first)
            #                kwargs['default'] = []
            #            else:
            d["type"] = lambda x: x
        else:
            d["action"] = "store"
            if type(default) in [type(None), str]:
                d["type"] = lambda x: x
            else:
                d["type"] = type(default)

        if param in helps:
            d["help"] = helps[param]

        if param in metavars:
            d["metavar"] = metavars[param]

        parser.add_argument(*args, **d)

    # Compulsary positional options
    for need in needed:

        d = {"action": "store", "type": lambda x: x}

        if need in helps:
            d["help"] = helps[need]

        if need in shorts:
            args = [shorts[need]]
        else:
            args = [need]

        parser.add_argument(*args, **d)

    # The trailing arguments
    if varargs:
        d = {"action": "store", "type": lambda x: x, "nargs": "*"}

        if varargs in helps:
            d["help"] = helps[varargs]

        if varargs in shorts:
            d["metavar"] = shorts[varargs]
        else:
            d["metavar"] = varargs

        parser.add_argument("__args", **d)

    return parser


def _correct_args(func, kwargs):
    """
        Convert a dictionary of arguments including __argv into a list
        for passing to the function.
    """
    args = inspect.getargspec(func)[0]
    return [kwargs[arg] for arg in args] + kwargs["__args"]


def entrypoint(func):
    frame_local = sys._getframe(1).f_locals
    if "__name__" in frame_local and frame_local["__name__"] == "__main__":
        argv = sys.argv[1:]

        parser = _signature_parser(func)
        kwargs = parser.parse_args(argv).__dict__

        # special cli flags

        # --version is handled by ArgParse
        # if kwargs.get('version'):
        #    print module_version(func)
        #    return
        if "version" in kwargs.keys():
            del kwargs["version"]

        # --debug
        FORMAT = "%(asctime)-6s: %(name)s - %(levelname)s - %(message)s"
        if kwargs.get("debug"):
            logging.basicConfig(
                level=logging.DEBUG, format=FORMAT,
            )
        del kwargs["debug"]

        if "__args" in kwargs:
            return func(*_correct_args(func, kwargs))
        else:
            return func(**kwargs)

    return func
