from pathlib import Path

import pandas as pd
import vectorbt as vbt


def decimal_to_datetime(dec: float) -> pd.Timestamp:
    year = int(dec)
    month = int(round((dec - year) * 100))
    return pd.Timestamp(year=year, month=month, day=1, tz="UTC")


def _download_data():
    price = vbt.SP500PriceData.download("P").get()
    earnings = vbt.SPEarningsData.download("E").get()
    cpi = vbt.CPIData.download("CPI").get()
    df = pd.concat([price, earnings, cpi], axis=1)
    return df["P"], df["E"], df["CPI"]


def test_sources_match_sheet():
    price, earnings, cpi = _download_data()
    csv_path = Path(__file__).resolve().parent / "resources" / "shiller_cape.csv"
    sheet = pd.read_csv(csv_path, skiprows=7)[["Date", "P", "E", "CPI"]].dropna()
    sheet[["P", "E", "CPI"]] = sheet[["P", "E", "CPI"]].apply(pd.to_numeric)
    sheet["Date"] = sheet["Date"].apply(decimal_to_datetime)
    sheet.set_index("Date", inplace=True)
    for date in ["2022-01-01", "2023-01-01"]:
        assert abs(price.loc[date] - sheet.loc[date, "P"]) < 1
        assert abs(earnings.loc[date] - sheet.loc[date, "E"]) < 50
        assert abs(cpi.loc[date] - sheet.loc[date, "CPI"]) < 1


def test_shiller_cape_matches_sheet():
    price, earnings, cpi = _download_data()
    sig = vbt.SHILLER_CAPE.run(price, earnings, cpi, lower=10, upper=30)
    cape = sig.cape
    csv_path = Path(__file__).resolve().parent / "resources" / "shiller_cape.csv"
    sheet = pd.read_csv(csv_path, skiprows=7)[["Date", "CAPE"]].dropna()
    sheet["CAPE"] = pd.to_numeric(sheet["CAPE"])
    sheet["Date"] = sheet["Date"].apply(decimal_to_datetime)
    sheet.set_index("Date", inplace=True)
    for date in ["2022-01-01", "2023-01-01"]:
        assert abs(cape.loc[date] - sheet.loc[date, "CAPE"]) < 10


def test_cape_signal_generator():
    price, earnings, cpi = _download_data()
    sig = vbt.SHILLER_CAPE.run(price, earnings, cpi, lower=20, upper=30)
    assert sig.entries.any()
    assert sig.exits.any()
