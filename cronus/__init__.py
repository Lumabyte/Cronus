__title__ = 'Chronus'
__author__ = 'lumabyte'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present Lumabyte'
__version__ = '0.0.1'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import logging
from typing import NamedTuple, Literal

from .bot import *
from .event import *
from .lifecycle import *
from .plugin import *
from .service import *
from .source import *
from .utils import *

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=2, minor=2, micro=0, releaselevel='alpha', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo
