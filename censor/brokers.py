# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0212,W0718,E0402,W0201,W0613,E1120,R0902


"brokering"


objs = []


def add(obj) -> None:
    objs.append(obj)


def announce(txt):
    for obj in objs:
        obj.announce(txt)

def byorig(orig):
    for obj in objs:
        if object.__repr__(obj) == orig:
            return obj
    return None


def bytype(typ):
    for obj in objs:
        if typ in object.__repr__(obj):
            return obj
    return None


def remove(obj) -> None:
    try:
        objs.remove(obj)
    except ValueError:
        pass
