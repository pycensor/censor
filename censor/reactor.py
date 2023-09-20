# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0212,W0718,E0402,W0201,W0613,E1120,R0902,W0105
# pylint: disable=W0703


"reactor"


import queue
import ssl
import threading


from .excepts import errors
from .message import ready
from .objects import Object
from .threads import launch


def __dir__():
    return (
            'Reactor',
            'dispatch',
           )


class Reactor(Object):

    errors = []

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()


    def handle(self, obj):
        func = self.cbs.get(obj.type, None)
        if func:
            obj._thr = launch(
                              callback,
                              func,
                              obj,
                              name=obj.type
                            )
        return obj

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                obj = self.poll()
                if obj is None:
                    self.stop()
                    continue
                self.handle(obj)
            except (ssl.SSLError, EOFError) as ex:
                exc = ex.with_traceback(ex.__traceback__)
                errors.append(exc)
                self.stop()
                self.start()


    def poll(self):
        return self.queue.get()

    def put(self, obj) -> None:
        self.queue.put_nowait(obj)

    def register(self, typ, func) -> None:
        self.cbs[typ] = func

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()
        self.put(None)


def callback(func, obj) -> None:
    try:
        func(obj)
    except Exception as exc:
        excp = exc.with_traceback(exc.__traceback__)
        Reactor.errors.append(excp)
        ready(obj)
