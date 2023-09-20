# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402,R0903


"log text"


import time


from ..message import reply
from ..objects import Object
from ..storage import find, sync
from ..utility import fntime, laps


def __dir__():
    return (
            "Log",
            "log"
           )


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    if not event.rest:
        nmr = 0
        for obj in find('log'):
            lap = laps(time.time() - fntime(obj.__fnm__))
            reply(event, f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            reply(event, 'no log')
        return
    obj = Log()
    obj.txt = event.rest
    sync(obj)
    reply(event, 'ok')
