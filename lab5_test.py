import pandas as pd
from lab5 import convert_dates, check_unique, check_no_missing, 


def test_check_unique():
    ids = pd.Series([11, 21, 35, 74])
    result = check_unique(ids)
    expected = pd.Series([True])

    assert result.equals(expected)


def test_check_no_missing():
    borough = pd.Series(["MANHATTAN", "BROOKLYN", "QUEENS"])
    result = check_no_missing(borough)
    expected = pd.Series([True])

    assert result.equals(expected)


def test_convert_dates():
    dates = pd.Series(["02/13/2025", "08/22/2025", "not-a-date"])
    result = convert_dates(dates)
    expected = pd.Series(pd.to_datetime(["02/13/2025", "08/22/2025", None], errors="coerce"))

    assert result.equals(expected) 
