# DuckDB SQL revenue regression

A DuckDB SQL transformation joins orders to campaign attribution. A subtle join bug duplicates
revenue for orders with multiple attribution rows.

Fix the SQL so `output/order_revenue.parquet` has one row per order and reconciles to source order
revenue.

Orders without attribution should remain in the output with a null channel. Multi-touch attribution
rows must be reduced to one selected channel before joining to revenue.
