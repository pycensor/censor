# This file is placed in the Public Domain.
#
# pylint: disable=C0116,E0402


"basic commands"


from ..command import cmds
from ..message import reply
from ..runtime import Cfg


def __dir__():
    return (
            "cmd",
            "ver"
           )


def cmd(event):
    reply(event, ",".join(sorted(cmds)))


def ver(event):
    reply(event, Cfg.description)
