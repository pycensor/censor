# This file is placed in the Public Domain.
#
# pylint: disable=C0116,W0105,E0402


"status of bots"


from ..brokers import objs
from ..message import reply


def __dir__():
    return (
            "sts",
           )


def sts(event):
    nmr = 0
    for bot in objs:
        if 'state' in dir(bot):
            reply(event, str(bot.state))
            nmr += 1
    if not nmr:
        reply(event, "no status")
