# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Consumer Price Index data sourced from FRED."""

import os
import pandas as pd
from fredapi import Fred

from vectorbt import _typing as tp
from vectorbt.data.base import Data
from vectorbt.utils.datetime_ import to_tzaware_datetime, get_utc_tz


def _get_fred_api_key() -> tp.Optional[str]:
    """Return FRED API key from env or secrets file."""
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        key_file = os.getenv("FRED_API_KEY_FILE", "/run/secrets/FRED_API_KEY")
        if os.path.exists(key_file):
            with open(key_file) as f:
                api_key = f.read().strip()
    return api_key


def _fred_series(series_id: str) -> pd.Series:
    fred = Fred(api_key=_get_fred_api_key())
    series = fred.get_series(series_id)
    series.index = pd.to_datetime(series.index).to_period("M").to_timestamp().tz_localize(get_utc_tz())
    return series.astype(float)


class CPIData(Data):
    """`Data` for CPI (CPIAUCNS) sourced from FRED."""

    @classmethod
    def download_symbol(
        cls,
        symbol: tp.Label = "CPI",
        start: tp.DatetimeLike = None,
        end: tp.DatetimeLike = None,
        **kwargs,
    ) -> tp.SeriesFrame:
        series = _fred_series("CPIAUCNS").rename(symbol)
        if start is not None:
            start = to_tzaware_datetime(start, tz=get_utc_tz())
            series = series.loc[series.index >= start]
        if end is not None:
            end = to_tzaware_datetime(end, tz=get_utc_tz())
            series = series.loc[series.index <= end]
        return series
