import duckdb

DB_FILE = "lab.duckdb"
SQL_FILE = "init_db.sql"

with open(SQL_FILE, "r") as f:
    sql = f.read()

con = duckdb.connect(DB_FILE)
con.execute(sql)
con.close()

print(f"Database initialized: {DB_FILE}")
