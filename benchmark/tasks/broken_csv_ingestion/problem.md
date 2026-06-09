# Broken CSV ingestion

The customer ingestion pipeline reads monthly CSV exports from a legacy CRM and should write
`output/customers.parquet`.

The starter pipeline is intentionally brittle. Fix it so it handles mixed column casing, dates,
numeric strings with thousands separators, missing values, duplicate customer rows, and deterministic
output ordering.

Run:

```bash
python -m pytest tests
```
