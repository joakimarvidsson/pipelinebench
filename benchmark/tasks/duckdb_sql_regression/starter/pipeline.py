from __future__ import annotations

from pathlib import Path

import duckdb


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    duckdb.sql(
        """
        COPY (
            SELECT
                o.order_id,
                o.customer_id,
                o.order_date,
                a.channel,
                o.revenue
            FROM read_csv_auto('seed_data/orders.csv') o
            JOIN read_csv_auto('seed_data/attribution.csv') a
              ON o.order_id = a.order_id
            ORDER BY o.order_id
        ) TO 'output/order_revenue.parquet' (FORMAT PARQUET)
        """
    )


if __name__ == "__main__":
    main()
