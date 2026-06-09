# Schema drift in Parquet ingestion

Daily account extracts arrive with reordered columns, changed integer/float representations, and
new nullable fields. The output contract must stay stable without silently dropping important new
fields.

Fix `starter/pipeline.py` so it reads every seed partition and writes `output/accounts.parquet` with
a stable schema.

The downstream contract expects `account_id`, `balance`, `is_active`, `opened_at`, and
`account_tier`. New nullable fields should be preserved when they are part of that contract rather
than dropped because an earlier partition did not contain them.
