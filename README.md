# Greenhouse Gas Reporting Program Emissions API Documentation

## Connecting to the API

Since we are running the API locally, access the endpoint at:

http://127.0.0.1:5000

(Or the address shown in your console when running the Flask app.)

---

## Welcome

**Method:** GET  
**Path:** `/`  
**Query parameters:** None  

This endpoint returns a simple welcome message confirming that the API is running.

### Example

http://127.0.0.1:5000/

---

## List Facilities and Emissions Data

**Source:** `ghgp_data_2023.csv`

**Method:** GET  
**Path:** `/api/list`

This endpoint returns facility-level greenhouse gas emissions data. Results can be filtered, paginated, and returned in JSON or CSV format.

This version of the API supports:

- Filtering on **string columns** (including values with spaces, like multi-word facility names)
- Filtering on **numeric columns**
- Filtering using **column names that contain spaces** (URL-encode spaces as `%20`)
- Pagination via `limit` and `offset`

---

### Query Parameters

- **format** (optional): `json` or `csv`  
  Default: `json`  
  Controls the output format.

- **filterby** (optional): Column name to filter by.  
  If provided, `filtervalue` must also be provided.

- **filtervalue** (optional): Value used to filter rows in the specified column.  
  Required when `filterby` is provided. Filtering uses exact matches.  
  For values with spaces, you can use `+` (or `%20`) in URLs.

- **limit** (optional): Maximum number of rows to return.  
  Default: `1000`

- **offset** (optional): Number of rows to skip before returning results.  
  Default: `0`

---

### Available Columns

You may use any of the following columns with `filterby`:

- Facility Id  
- FRS Id  
- Facility Name  
- City  
- State  
- Zip Code  
- Address  
- County  
- Latitude  
- Longitude  
- Primary NAICS Code  
- Industry Type (subparts)  
- Industry Type (sectors)  
- Total reported direct emissions  
- CO2 emissions (non-biogenic)  
- Methane (CH4) emissions  
- Nitrous Oxide (N2O) emissions  
- HFC emissions  
- PFC emissions  
- SF6 emissions  
- NF3 emissions  
- Other Fully Fluorinated GHG emissions  
- HFE emissions  
- Very Short-lived Compounds emissions  
- Other GHGs (metric tons CO2e)  
- Biogenic CO2 emissions (metric tons)  
- Stationary Combustion  
- Electricity Generation  
- Adipic Acid Production  
- Aluminum Production  
- Ammonia Manufacturing  
- Cement Production  
- Electronics Manufacture  
- Ferroalloy Production  
- Fluorinated GHG Production  
- Glass Production  
- HCFC–22 Production from HFC–23 Destruction  
- Hydrogen Production  
- Iron and Steel Production  
- Lead Production  
- Lime Production  
- Magnesium Production  
- Miscellaneous Use of Carbonates  
- Nitric Acid Production  
- Petroleum and Natural Gas Systems – Offshore Production  
- Petroleum and Natural Gas Systems – Processing  
- Petroleum and Natural Gas Systems – Transmission/Compression  
- Petroleum and Natural Gas Systems – Underground Storage  
- Petroleum and Natural Gas Systems – LNG Storage  
- Petroleum and Natural Gas Systems – LNG Import/Export  
- Petrochemical Production  
- Petroleum Refining  
- Phosphoric Acid Production  
- Pulp and Paper Manufacturing  
- Silicon Carbide Production  
- Soda Ash Manufacturing  
- Titanium Dioxide Production  
- Underground Coal Mines  
- Zinc Production  
- Municipal Landfills  
- Industrial Wastewater Treatment  
- Manufacture of Electric Transmission and Distribution Equipment  
- Industrial Waste Landfills  
- Is some CO2 collected on-site and used to manufacture other products and therefore not emitted from the affected manufacturing process unit(s)? (as reported under Subpart G or S)  
- Is some CO2 reported as emissions from the affected manufacturing process unit(s) under Subpart AA, G or P collected and transferred off-site or injected (as reported under Subpart PP)?  
- Does the facility employ continuous emissions monitoring?  

---

## Example Queries (Working Links)

### 1) Return first 5 rows in JSON

http://127.0.0.1:5000/api/list?format=json&limit=5

### 2) Filter by a column name with spaces + a multi-word facility name (example:AJAX PLANT)

http://127.0.0.1:5000/api/list?format=json&filterby=Facility%20Name&filtervalue=AJAX+PLANT&limit=5

### 3) Same query as above, but return CSV

http://127.0.0.1:5000/api/list?format=csv&filterby=Facility%20Name&filtervalue=AJAX+PLANT&limit=5

### 4) Pagination example: skip the first 2 rows and return the next 5

http://127.0.0.1:5000/api/list?format=json&limit=5&offset=2

---

### Error Handling

The API returns a plain-text error message if:

- `filterby` is not a valid column  
- `filtervalue` is missing when `filterby` is provided  
- `format` is not `json` or `csv`  

---

## Notes

- Filtering uses exact matches.
- If you include `filterby`, you must include `filtervalue`.
- For column names with spaces, encode spaces as `%20` (e.g., `Facility%20Name`).
- For filter values with spaces, use `+` or `%20` (e.g., `AJAX+PLANT`).
- Pagination is handled with `limit` and `offset`.
- JSON output is returned as a list of records.
- CSV output is returned as raw CSV text.
