# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,R0903,W0105,E0402


"todo list"


import time


from ..message import reply
from ..objects import Object
from ..storage import find, sync
from ..utility import fntime, laps


def __dir__():
    return (
            "Todo",
            "dne",
            "tdo"
           )


class Todo(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ''


def dne(event):
    if not event.args:
        reply(event, "dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for obj in find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        sync(obj)
        reply(event, 'ok')
        break
    if not nmr:
        reply(event, "nothing todo")


def tdo(event):
    if not event.rest:
        nmr = 0
        for obj in find('todo'):
            lap = laps(time.time()-fntime(obj.__fnm__))
            reply(event, f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            reply(event, "no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    sync(obj)
    reply(event, 'ok')
