# This file is placed in the Public Domain.
#
# pylint: disable=C0116,E0402


"errors"


import io
import traceback


from ..excepts import errors
from ..message import reply


def __dir__():
    return (
            "err",
           )


def err(event):
    if not errors:
        reply(event, "no errors")
        return
    for exc in errors:
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            reply(event, line)
