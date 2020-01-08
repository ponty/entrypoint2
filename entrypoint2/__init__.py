from __future__ import with_statement
# from contextlib import nested
from decorator import decorator
import argparse
import textwrap
import codecs
import inspect
import re
import sys
import logging


"""
    This is a library of decorators designed for writing scripts quickly. This
    means they are not the most sustainable tools that exist, but they do what
    they do well, and with minimal fuss. If you want additional features, you
    are likely to have more fun if you stop being lazy and using
    this library :p.

    Everything here uses unicode strings, and opens files for unicode access.
    You can change the ENCODING property of this module from "utf8" if you
    need to.

    There are three core parts of functionality:

    Auto-run the main function when __name__ == '__main__'.
        @autorun, @entrypoint, @entrywithfile

    Parse command-line arguments from a function's signature.
        signature_parser, @acceptargv, @entrypoint, @entrywithfile

    Manage files to be passed to a function.
        @withfile, @entrywithfile


    A typical use will be something like this:

    import sys
    from entrypoint import entrypoint, withfile

    @entrypoint
    @withfile(tsv='r', csv='w')
    def main(tsv, csv, verbose=False):
        '''
            Converts a tab-separated-values file into comma-separated-values
            with the usual disregard for escaping conventions in those formats.

            tsv: The input tab-separated file
            csv: The output comma-separated file
            --verbose -v: Print progress report
        '''
        lineno = 1
        for line in tsv:
            print >>csv, ",".join(line.split("\t"))
            lineno += 1
            if verbose and not lineno % 10:
                print >>sys.stderr, "line %s" % lineno
"""


ENCODING = 'utf8'

PY3 = sys.version_info[0] >= 3


def unidecode(x):
    if PY3:
        return x
    else:
        return x.decode(ENCODING)


def module_version(func):
    version = None
    for v in '__version__ VERSION version'.split():
        if PY3:
            version = func.__globals__.get(v)
        else:
            version = func.func_globals.get(v)
        if version:
            break
    return version


class ParagraphPreservingArgParseFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super(ParagraphPreservingArgParseFormatter,
              self).__init__(*args, **kwargs)
        self._long_break_matcher = argparse._re.compile(r'\n\n+')

    def _fill_text(self, text, width, indent):
        output = []
        for block in self._long_break_matcher.split(text.strip()):
            output.append(textwrap.fill(block, width,
                                        initial_indent=indent, subsequent_indent=indent))
        return "\n\n".join(output + [''])


class UsageError(Exception):
    """
        When a function wrapped with @acceptargv or @entrypoint raises this
        exception, the message will be printed to the user implying that it was
        their fault that things have gone horribly wrong.
    """

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message
    pass


class FileUsageError(UsageError):

    def __init__(self, e):
        """
            Convert an IOError into a UsageError.
        """
        super(Exception, self).__init__(e)
        self.message = "%s: '%s'" % (e.strerror, e.filename)


class SpecError(TypeError):
    """
        Used for define-time errors with withfile specs.
    """
    pass


def _parse_doc(docs):
    """
        Converts a well-formed docstring into documentation
        to be fed into argparse.

        See signature_parser for details.

        shorts: (-k for --keyword -k, or "from" for "frm/from")
        metavars: (FILE for --input=FILE)
        helps: (docs for --keyword: docs)
        description: the stuff before
        epilog: the stuff after
    """

    name = "(?:[a-zA-Z][a-zA-Z0-9-_]*)"

    re_var = re.compile(r"^ *(%s)(?: */(%s))? *:(.*)$" % (name, name))
    re_opt = re.compile(r"^ *(?:(-[a-zA-Z0-9]),? +)?--(%s)(?: *=(%s))? *:(.*)$"
                        % (name, name))

    shorts, metavars, helps, description, epilog = {}, {}, {}, "", ""

    if docs:

        for line in docs.split("\n"):

            line = line.strip()

            # remove starting ':param'
            if line.startswith(':param'):
                line = line[len(':param'):]

            # skip ':rtype:' row
            if line.startswith(':rtype:'):
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


def signature_parser(func):
    """
        Creates an argparse.ArgumentParser from the function's signature.

        Arguments with no default are compulsary positional arguments,
        Arguments with defaults are optional --flags.

        If the default is True or False, the action of the flag will
        toggle the argument and the flag takes no parameters.

        If the default is None or a unicode string, the flag takes a
        string argument that passed to the function as a unicode string
        decoded using entrypoint.ENCODING

        If the default is a string, then the argument is passed as a binary
        string (be careful!), an int and a float cause parsing of those too.

        If you want the arguments to be a file, consider using the
        @withfile decorator.

        Documentation can be read out of the function's docstring, which should
        be of the basic form:
        '''
            A short introduction to your program.

                arg: Help for positional parameter.
                frm/from: Help for a positional parameter
                          with a reserved public name
                          (i.e. this displays to the user as "from"
                          but sets the "frm" variable)
                --opt: Help for optional parameter.
                -f --flag: An optional parameter that has a short version.
                --mode=MODE: An optional parameter that takes a MODE
                -t --type: A combination of both of the above, and one
                                which requires continuing of the documentation
                                on an indented line

            An epilog explaining anything you feel needs further clarity.

            ----

            Any documentation for the function itself that isn't covered by the
            public documentation above the line.
        '''

        All sections, and indeed the presence of a docstring, are not required.

        NOTE: for this to work, the function's signature must be in-tact
              some decorators (like @acceptargv for example) destroy, or
              mutilate the signature.
    """

    args, trail, kwargs, defaults = inspect.getargspec(func)

    if not args:
        args = []

    if not defaults:
        defaults = []

    if kwargs:
        raise Exception("Can't wrap a function with **kwargs")

    # Compulsary positional options
    needed = args[0:len(args) - len(defaults)]

    # Optional flag options
    params = args[len(needed):]

    shorts, metavars, helps, description, epilog = _parse_doc(func.__doc__)

    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=ParagraphPreservingArgParseFormatter)

    # special flags
    special_flags = []

    special_flags += ['debug']
    defaults += (False,)
    helps['debug'] = 'set logging level to DEBUG'
    if module_version(func):
        special_flags += ['version']
        defaults += (False,)
        helps['version'] = "show program's version number and exit"
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
                    short = '-' + first_char
        # -h conflicts with 'help'
        if short and short != '-h':
            args = [short] + args

        kwargs = {'default': default, 'dest': param.replace("-", "_")}

        if param == 'version':
            kwargs['action'] = 'version'
            kwargs['version'] = module_version(func)
        elif default is True:
            kwargs['action'] = 'store_false'
        elif default is False:
            kwargs['action'] = 'store_true'
        elif isinstance(default, list):
            kwargs['action'] = 'append'
#  default is not working
#            if len(default):
#                first = default[0]
#                if type(first) in [type(None), unicode]:
#                    kwargs['type'] = unidecode
#                else:
#                    kwargs['type'] = type(first)
#                kwargs['default'] = []
#            else:
            kwargs['type'] = unidecode
        else:
            kwargs['action'] = 'store'
            if type(default) in [type(None), str if PY3 else unicode]:
                kwargs['type'] = unidecode
            else:
                kwargs['type'] = type(default)

        if param in helps:
            kwargs['help'] = helps[param]

        if param in metavars:
            kwargs['metavar'] = metavars[param]

        parser.add_argument(*args, **kwargs)

    # Compulsary positional options
    for need in needed:

        kwargs = {'action': 'store', 'type': unidecode}

        if need in helps:
            kwargs['help'] = helps[need]

        if need in shorts:
            args = [shorts[need]]
        else:
            args = [need]

        parser.add_argument(*args, **kwargs)

    # The trailing arguments
    if trail:
        kwargs = {'action': 'store', 'type': unidecode, 'nargs': "*"}

        if trail in helps:
            kwargs['help'] = helps[trail]

        if trail in shorts:
            kwargs['metavar'] = shorts[trail]
        else:
            kwargs['metavar'] = trail

        parser.add_argument('__args', **kwargs)

    return parser


def _correct_args(func, kwargs):
    """
        Convert a dictionary of arguments including __argv into a list
        for passing to the function.
    """
    args = inspect.getargspec(func)[0]
    return [kwargs[arg] for arg in args] + kwargs['__args']


def entrypoint(func):
    """
        A decorator for your main() function.

        Really a combination of @autorun and @acceptargv, so will run the
        function if __name__ == '__main__' with arguments extricated from
        argparse.

        As with @acceptargv, this must either be the innermost decorator, or
        separated only by "well-behaved" decorators that preserve the __doc__
        attribute AND the function signature.

        As with @autorun, this must be theoutermost decorator, as any
        decorators further out will not be applied to the function until after
        it is run.
    """
    frame_local = sys._getframe(1).f_locals
    if '__name__' in frame_local and frame_local['__name__'] == '__main__':
        argv = sys.argv[1:]

        parser = signature_parser(func)
        try:
            kwargs = parser.parse_args(argv).__dict__

            # special cli flags

            # --version is handled by ArgParse
            # if kwargs.get('version'):
            #    print module_version(func)
            #    return
            if 'version' in kwargs.keys():
                del kwargs['version']

            # --debug
            FORMAT = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
            if kwargs.get('debug'):
                logging.basicConfig(
                    level=logging.DEBUG,
                    format=FORMAT,
                )
            del kwargs['debug']

            if "__args" in kwargs:
                return func(*_correct_args(func, kwargs))
            else:
                return func(**kwargs)

        except UsageError as e:
            parser.error(e.message)

    return func


def autorun(func, _depth=1):
    """
        Runs the function if the module in which it is declared is being run
        directly from the commandline. Putting the following after the function
        definition would be similar:

        if __name__ == '__main__':
            func()

        NOTE: This will work most expectedly as the outermost decorator, as it
        will call the function before any more outwards decorators have been
        applied.
    """

    frame_local = sys._getframe(_depth).f_locals
    if '__name__' in frame_local and frame_local['__name__'] == '__main__':
        func(argv=sys.argv[1:])

    return func


def acceptargv(func):
    """
        Transforms the signature of the function, and it's associated __doc__
        into an argparse-parser, then calls the function with the results of
        using said parser.

        The function returned takes an optional argument, which is the list of
        parameters, if they are not given, sys.argv[1:] is used instead.

        The function may raise a UsageError() if it wants to signal an error
        that the user has made with the parameters, this is done by
        @withuserfile for example.

        CAVEAT: this relies on the argument signature of the function, if that
                has been destroyed, perhaps by a badly behaved decorator, this
                won't work as expected.

        CAVEAT2: this destroys the argument signature of the function ;)
    """

    parser = signature_parser(func)

    def main(*args, **kw):
        argv = kw.get('argv', None)
        if argv == None:
            return func(*args, **kw)
        else:
            try:
                kwargs = parser.parse_args(argv).__dict__

                # special cli flags

                # --version is handled by ArgParse
                # if kwargs.get('version'):
                #    print module_version(func)
                #    return
                if 'version' in kwargs.keys():
                    del kwargs['version']

                # --debug
                if kwargs.get('debug'):
                    logging.basicConfig(level=logging.DEBUG)
                del kwargs['debug']

                if "__args" in kwargs:
                    return func(*_correct_args(func, kwargs))
                else:
                    return func(**kwargs)
            except UsageError as e:
                parser.error(e.message)

    main.__doc__ = func.__doc__
    main.__name__ = func.__name__
    main.__module__ = func.__module__
    main.__dict__ = func.__dict__.copy()

    return main


__all__ = ['UsageError', 'FileUsageError', 'acceptargv', 'argparse',
           'autorun', 'entrypoint', 'entrywithfile', 'runwithfile',
           'signature_parser', 'withfile', 'withuserfile']
