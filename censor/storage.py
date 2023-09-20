# This file is placed in the Public Domain.
#
# pylint: disable=C0112,C0115,C0116,W0105,R0903,E0402,C0209


"persistence"


import datetime
import inspect
import os
import uuid


from .objects import Object, fqn, keys, read, search, update, write
from .utility import cdir, fntime, strip


"defines"


def __dir__():
    return (
            'fetch',
            'find',
            'fntime',
            'sync'
           )


__all__ = __dir__()


classes = {}
workdir = os.path.expanduser('~/.%s' % __file__.split(os.sep)[-2])


"utility"


def add(clz):
    if not clz:
        return
    name = str(clz).split()[1][1:-2]
    classes[name] = clz


def find(mtc, selector=None) -> []:
    if selector is None:
        selector = {}
    for fnm in reversed(sorted(fns(mtc), key=fntime)):
        obj = Object()
        fetch(obj, fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        obj.__fnm__ = fnm
        yield obj


def fns(mtc) -> []:
    dname = ''
    clz = long(mtc)
    pth = None
    if clz:
        pth = path(clz)
    else:
        pth = workdir
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            dname = sorted(dirs)[-1]
            if dname.count('-') == 2:
                ddd = os.path.join(rootdir, dname)
                fls = sorted(os.listdir(ddd))
                if fls:
                    yield strip(os.path.join(ddd, fls[-1]))

def long(name):
    split = name.split(".")[-1].lower()
    res = None
    for named in keys(classes):
        if split in named.split(".")[-1].lower():
            res = named
            break
    return res


def path(pth):
    cdir(pth)
    return os.path.join(store(), pth)


def scan(mod) -> None:
    for key, clz in inspect.getmembers(mod, inspect.isclass):
        if key.startswith("cb"):
            continue
        if not issubclass(clz, Object):
            continue
        add(clz)


def store(pth=""):
    return os.path.join(workdir, "store", pth)


"methods"


def fetch(obj, pth):
    pth2 = store(pth)
    return read(obj, pth2)


def ident(obj) -> str:
    return os.path.join(
                        fqn(obj),
                        str(uuid.uuid4().hex),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x.__fnm__)
                   )
    if result:
        inp = result[-1]
        update(obj, inp)
        if "__fnm__" in inp:
            obj.__fnm__ = inp.__fnm__


def sync(obj, pth=None):
    if "__fnm__" in obj:
        pth = obj.__fnm__
        del obj.__fnm__
    if not pth:
        pth = ident(obj)
    pth = store(pth)
    cdir(pth)
    write(obj, pth)
    obj.__fnm__ = pth
