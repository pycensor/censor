# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0212,E0402,W0201,W0613,E1120,R0902,W0105,W0612
# pylint: disable=W0718


"command"


import inspect


from .excepts import errors
from .message import ready, show
from .objects import Object
from .parsing import parse


"defines"


def __dir__():
    return (
            'add',
            'command',
            'scan',
           )


__all__ = __dir__()


cmds = Object()


"utility"


def add(func):
    cmds[func.__name__] = func


def scan(mod) -> None:
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            add(cmd)


"methods"


def command(obj):
    parse(obj, obj.txt)
    obj.type = "command"
    func = getattr(cmds, obj.cmd, None)
    if func:
        try:
            func(obj)
            show(obj)
        except Exception as ex:
            exc = ex.with_traceback(ex.__traceback__)
            errors.append(exc)
    ready(obj)
