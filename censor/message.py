# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0212,E0402,W0201,W0613,E1120,R0902,W0105,W0612
# pylint: disable=W0718,C0103


"messaging"


from .brokers import byorig


def __dir__():
    return (
            'ready',
            'reply',
            'wait'
           )


__all__ = __dir__()


def ready(obj) -> None:
    if "_ready" in obj:
        obj._ready.set()


def reply(obj, txt) -> None:
    if "result" in obj:
        obj.result.append(txt)


def show(obj):
    if "channel" not in obj:
        channel = ""
    else:
        channel = obj.channel
    bot = byorig(obj.orig)
    if bot:
        for txt in obj.result:
            bot.say(channel, txt)


def wait(obj) -> []:
    if "_thr" in obj:
        obj._thr.join()
    if "_ready" in obj:
        obj._ready.wait()
    if "_result" in obj:
        return obj._result
    return []
