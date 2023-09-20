# This file is placed in the Public Domain.
#
# pylint: disable=C0413


"unittest"

import os
import sys


sys.path.insert(0, os.getcwd())


import censor.storage


censor.storage.workdir = ".test"
