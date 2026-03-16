import duckdb

con = duckdb.connect("lab.duckdb")

print("\nTables in the database:")
print(con.execute("SHOW TABLES").fetchdf())

print("\nSample rows from ghgp_data:")
print(con.execute("SELECT * FROM ghgp_data LIMIT 5").fetchdf())

print("\nUsers table:")
print(con.execute("SELECT * FROM users").fetchdf())

con.close()
