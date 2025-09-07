# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""S&P 500 earnings data sourced from multpl.com."""

import pandas as pd

from vectorbt import _typing as tp
from vectorbt.data.base import Data
from vectorbt.utils.datetime_ import to_tzaware_datetime, get_utc_tz


def _multpl_series(path: str) -> pd.Series:
    url = f"https://www.multpl.com/{path}/table/by-month"
    df = pd.read_html(url, header=0)[0]
    df = df.dropna()
    df.columns = ["Date", "value"]
    dates = pd.PeriodIndex(pd.to_datetime(df["Date"]), freq="M").to_timestamp()
    df["Date"] = dates
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    df = df[~df.index.duplicated(keep="first")]
    df.index = df.index.tz_localize(get_utc_tz())
    return df["value"].astype(float)


class SPEarningsData(Data):
    """`Data` for S&P 500 earnings sourced from multpl.com."""

    @classmethod
    def download_symbol(
        cls,
        symbol: tp.Label = "E",
        start: tp.DatetimeLike = None,
        end: tp.DatetimeLike = None,
        **kwargs,
    ) -> tp.SeriesFrame:
        series = _multpl_series("s-p-500-earnings").rename(symbol)
        if start is not None:
            start = to_tzaware_datetime(start, tz=get_utc_tz())
            series = series.loc[series.index >= start]
        if end is not None:
            end = to_tzaware_datetime(end, tz=get_utc_tz())
            series = series.loc[series.index <= end]
        return series
