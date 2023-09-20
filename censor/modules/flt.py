# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402


"list of bots"


from ..brokers import objs
from ..message import reply


def __dir__():
    return (
            "flt",
           )


def flt(event):
    try:
        index = int(event.args[0])
        reply(event, str(objs[index]))
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    reply(event,
                ' | '.join([repr(obj).split()[0].split(".")[-1]
                            for obj in objs])
               )
