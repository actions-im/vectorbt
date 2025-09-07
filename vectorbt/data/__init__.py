# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Modules for working with data sources."""

from vectorbt.data.base import symbol_dict, Data
from vectorbt.data.custom import SyntheticData, GBMData, YFData, BinanceData, CCXTData, AlpacaData
from vectorbt.data.sp500_price import SP500PriceData
from vectorbt.data.cpi import CPIData
from vectorbt.data.sp500_earnings import SPEarningsData
from vectorbt.data.updater import DataUpdater

__all__ = [
    'symbol_dict',
    'Data',
    'DataUpdater',
    'SyntheticData',
    'GBMData',
    'YFData',
    'BinanceData',
    'CCXTData',
    'AlpacaData',
    'SP500PriceData',
    'CPIData',
    'SPEarningsData'
]

__pdoc__ = {k: False for k in __all__}
