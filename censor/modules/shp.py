# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0105,E0402,R0903


"shopping list"


import time


from ..message import reply
from ..objects import Object
from ..storage import find, sync
from ..utility import fntime, laps


def __dir__():
    return (
            "got",
            "sop"
           )


class Shop(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def got(event):
    if not event.args:
        reply(event, "got <txt>")
        return
    selector = {'txt': event.args[0]}
    nrs = 0
    for obj in find('shop', selector):
        nrs += 1
        obj.__deleted__ = True
        sync(obj)
        reply(event, 'ok')
    if not nrs:
        reply(event,  "no shops")


def shp(event):
    if not event.rest:
        nmr = 0
        for obj in find('shop'):
            lap = laps(time.time()-fntime(obj.__fnm__))
            reply(event, f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            reply(event, "no shops")
        return
    obj = Shop()
    obj.txt = event.rest
    sync(obj)
    reply(event, 'ok')
