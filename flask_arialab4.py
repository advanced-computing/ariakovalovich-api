from flask import Flask, request, Response
import pandas as pd

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Return a friendly HTTP greeting."""
    return "<p>Hello, World!</p>"


@app.get("/api/list")
def list_api():
    # Get the query parameters
    out_format = request.args.get("format", "json").lower()
    filterby = request.args.get("filterby", None)
    filtervalue = request.args.get("filtervalue", None)
    limit = int(request.args.get("limit", 1000))
    offset = int(request.args.get("offset", 0))

    # Load the data
    data = pd.read_csv("ghgp_data_2023.csv")

    # Make column-name matching tolerant of leading/trailing spaces
    data.columns = data.columns.str.strip()

    # Filter the data (supports strings with spaces, e.g. "Facility Name=Big Plant LLC")
    data = filter_by_value(data, filterby, filtervalue)
    if isinstance(data, str):
        return Response(data, mimetype="text/plain", status=400)

    # Apply limit and offset (pagination)
    data = apply_limit_offset(data, limit, offset)

    # Convert to the requested format and return
    return convert_to_format(data, out_format)


def filter_by_value(data: pd.DataFrame, filterby: str | None, filtervalue: str | None):
    if not filterby:
        return data

    filterby = filterby.strip()

    if filtervalue is None:
        return "Invalid filtervalue"
    if filterby not in data.columns:
        return "Invalid filterby column"

    # Normalize the filter value (handles accidental leading/trailing spaces,
    # and URL-encoded spaces are automatically decoded by Flask)
    fv_raw = str(filtervalue).strip()

    col = data[filterby]

    # If the column is numeric-like, try numeric comparison first.
    # Otherwise do a robust string comparison (good for multi-word facility names).
    if pd.api.types.is_numeric_dtype(col):
        fv_num = pd.to_numeric(fv_raw, errors="coerce")
        if pd.isna(fv_num):
            return "Invalid filtervalue for numeric column"
        return data[col == fv_num]

    # String (object) columns: compare as strings, trimming whitespace
    col_str = col.astype(str).str.strip()
    return data[col_str == fv_raw]


def apply_limit_offset(data: pd.DataFrame, limit: int, offset: int):
    # Guard against negative inputs
    limit = max(0, limit)
    offset = max(0, offset)
    return data.iloc[offset : offset + limit]


def convert_to_format(data: pd.DataFrame, out_format: str):
    if out_format == "json":
        return Response(data.to_json(orient="records"), mimetype="application/json")
    elif out_format == "csv":
        return Response(data.to_csv(index=False), mimetype="text/csv")
    else:
        return Response("Invalid format", mimetype="text/plain", status=400)


if __name__ == "__main__":
    app.run(debug=True)
