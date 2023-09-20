# This file is placed in the Public Domain.
#
#

"reinforcement degrades performance"


from .objects import Object
from .utility import skip


class Censor(Object):

    skip = []

    @staticmethod
    def doskip(txt):
        return skip(txt, Censor.skip)
