# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402,W0212,R1710,W0611,E0611,R0903,W0105,C0103
# pylint: disable=E0401,W0102
# ruff: noqa: F401


"console"


import readline
import sys
import threading
import _thread


from .clients import Client, command
from .message import wait


prompting = threading.Event()


class CLI(Client):

    def raw(self, txt):
        print(txt)


class Console(CLI):

    def __init__(self):
        CLI.__init__(self)
        self.prompting = threading.Event()

    def announce(self, txt):
        pass

    def handle(self, obj):
        command(obj)
        wait(obj)

    def prompt(self):
        self.prompting.set()
        inp = input("> ")
        self.prompting.clear()
        return inp

    def poll(self):
        try:
            return self.event(self.prompt())
        except EOFError:
            _thread.interrupt_main()

    def raw(self, txt):
        if self.prompting.is_set():
            txt = "\n" + txt
        print(txt)
        self.prompting.clear()
        sys.stdout.flush()
