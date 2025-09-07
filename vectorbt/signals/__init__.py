# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Modules for working with signals, such as entry and exit signals."""

from vectorbt.signals.enums import *
from vectorbt.signals.factory import SignalFactory
from vectorbt.signals.generators import (
    RAND,
    RANDX,
    RANDNX,
    RPROB,
    RPROBX,
    RPROBCX,
    RPROBNX,
    STX,
    STCX,
    OHLCSTX,
    OHLCSTCX,
    SHILLER_CAPE
)

__all__ = [
    'SignalFactory',
    'RAND',
    'RANDX',
    'RANDNX',
    'RPROB',
    'RPROBX',
    'RPROBCX',
    'RPROBNX',
    'STX',
    'STCX',
    'OHLCSTX',
    'OHLCSTCX',
    'SHILLER_CAPE'
]

__pdoc__ = {k: False for k in __all__}
