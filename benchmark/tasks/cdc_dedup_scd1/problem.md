# CDC deduplication for SCD1 current state

The input event stream contains inserts, updates, deletes, duplicate delivery, and out-of-order
timestamps. Produce the current customer dimension table at `output/customer_dimension.parquet`.

The latest event per customer wins. Deleted customers should not appear in the current-state output.
