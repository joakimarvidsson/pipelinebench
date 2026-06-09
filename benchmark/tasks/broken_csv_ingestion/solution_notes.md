# Maintainer solution notes

Normalize column names, concatenate all CSV files, parse dates with coercion, strip commas from
numeric strings, keep the newest deterministic customer record, fill missing lifetime value with
`0.0`, and sort by `customer_id` before writing Parquet.
