import pandas as pd


def check_unique(series: pd.Series):
    return pd.Series([series.is_unique])


def check_no_missing(series: pd.Series):
    return pd.Series([series.notna().all()])


def parse_dates(series: pd.Series):
    return pd.to_datetime(series, errors="coerce")
