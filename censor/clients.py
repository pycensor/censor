# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0212,E0402,W0201,W0613,E1120,R0902,W0105,W0612
# pylint: disable=W0718


"client"


import time


from .brokers import add
from .command import command
from .objects import Object
from .reactor import Reactor


def __dir__():
    return (
            'Client',
           )


__all__ = __dir__()


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)
        add(self)

    def announce(self, txt):
        self.raw(txt)

    def event(self, txt):
        evt = Object()
        evt.txt = txt
        evt.orig = object.__repr__(self)
        evt.type = "command"
        return evt

    def forever(self):
        while 1:
            time.sleep(1.0)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
