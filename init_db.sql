-- Drop and recreate the main table from the CSV
DROP TABLE IF EXISTS ghgp_data_2023;

CREATE TABLE ghgp_data AS
SELECT *
FROM read_csv_auto('ghgp_data_2023.csv', HEADER=TRUE);

-- Create users table
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username VARCHAR,
    age INTEGER,
    country VARCHAR
);