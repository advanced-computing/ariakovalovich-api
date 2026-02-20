import io
import pandas as pd

from flask_arialab4 import filter_by_value, apply_limit_offset, convert_to_format


def get_test_df():
    # Notes:
    # - Includes column names with spaces (e.g., "Facility Id", "Facility Name")
    # - Includes string fields with spaces in values (e.g., "AJAX PLANT")
    # - Includes numeric columns (e.g., emissions, lat/long)

    data = {
        "Facility Id": [1013701, 1012037, 1010475],
        "FRS Id": ["110070931003", "110063753656", ""],
        "Facility Name": ["30-30 Gas Plant", "50 Buttes Gas Plant", "AJAX PLANT"],
        "City": ["Plains", "Gillette", "Wheeler"],
        "State": ["TX", "WY", "TX"],
        "Zip Code": [79355, 82716, 79014],
        "Address": ["2300 FM 1622", "3669 South Hwy 50", "16600 CR N"],
        "County": ["YOAKUM COUNTY", "CAMPBELL COUNTY", ""],
        "Latitude": [33.05, 43.85, 35.55],
        "Longitude": [-102.89, -105.78, -100.12],
        "Primary NAICS Code": [211130, 213112, 211130],
        "Industry Type (subparts)": ["C,PP,RR (RPT),W-PROC", "C,W-PROC", "C,W-PROC"],
        "Industry Type (sectors)": [
            "Injection of CO2,Petroleum and Natural Gas Systems,Suppliers of CO2",
            "Petroleum and Natural Gas Systems",
            "Petroleum and Natural Gas Systems",
        ],
        "Total reported direct emissions": [44170.546, 61389.032, 38738.508],
        "CO2 emissions (non-biogenic)": [43895.8, 58078.3, 38053.6],
        "Methane (CH4) emissions": [259.25, 3278.25, 663.75],
        "Nitrous Oxide (N2O) emissions": [15.496, 32.482, 21.158],
        "Does the facility employ continuous emissions monitoring?": ["N", "N", "N"],
    }
    return pd.DataFrame(data)


def _text(maybe_response):
    """
    convert_to_format may return either:
    - a Flask Response object
    - or a plain string

    This helper extracts the text in either case.
    """
    if hasattr(maybe_response, "get_data"):
        return maybe_response.get_data(as_text=True)
    return maybe_response


def _normalize_for_compare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize dataframes before comparison to avoid false failures from:
    - dtype differences after CSV/JSON round-tripping (e.g., ints vs floats)
    - whitespace differences (e.g., 'N' vs 'N       ')
    """
    out = df.reset_index(drop=True).copy()
    for col in out.columns:
        out[col] = out[col].astype(str).str.strip()
    return out


def test_filter_by_value_facility_name_with_spaces_in_column_name_and_value():
    df = get_test_df()
    result = filter_by_value(df, "Facility Name", "AJAX PLANT").reset_index(drop=True)

    expected = df[df["Facility Name"] == "AJAX PLANT"].reset_index(drop=True)
    assert result.equals(expected)


def test_filter_by_value_state_string():
    df = get_test_df()
    result = filter_by_value(df, "State", "TX").reset_index(drop=True)

    expected = df[df["State"] == "TX"].reset_index(drop=True)
    assert result.equals(expected)


def test_filter_by_value_numeric_facility_id():
    df = get_test_df()
    # filter_by_value accepts strings (like query params), so we test with "1010475"
    result = filter_by_value(df, "Facility Id", "1010475").reset_index(drop=True)

    expected = df[df["Facility Id"] == 1010475].reset_index(drop=True)
    assert result.equals(expected)


def test_filter_by_value_invalid_column():
    df = get_test_df()
    result = filter_by_value(df, "NotARealColumn", "anything")
    assert result == "Invalid filterby column"


def test_filter_by_value_missing_filtervalue():
    df = get_test_df()
    result = filter_by_value(df, "State", None)
    assert result == "Invalid filtervalue"


def test_apply_limit_offset():
    df = get_test_df()
    # offset=1, limit=1 should return the 2nd row only
    result = apply_limit_offset(df, limit=1, offset=1).reset_index(drop=True)
    expected = df.iloc[1:2].reset_index(drop=True)
    assert result.equals(expected)


def test_convert_to_format_csv_roundtrip():
    df = get_test_df().head(2)

    out = convert_to_format(df, "csv")
    csv_text = _text(out)

    parsed = pd.read_csv(io.StringIO(csv_text))

    assert _normalize_for_compare(parsed).equals(_normalize_for_compare(df))


def test_convert_to_format_json_roundtrip():
    df = get_test_df().head(2)

    out = convert_to_format(df, "json")
    json_text = _text(out)

    parsed = pd.read_json(io.StringIO(json_text))
    parsed = parsed[df.columns]  # keep same column order

    assert _normalize_for_compare(parsed).equals(_normalize_for_compare(df))


def test_convert_to_format_invalid():
    df = get_test_df().head(1)

    out = convert_to_format(df, "invalid")
    body = _text(out)

    # Works whether you return a string or Response("Invalid format", ...)
    assert "Invalid format" in body
