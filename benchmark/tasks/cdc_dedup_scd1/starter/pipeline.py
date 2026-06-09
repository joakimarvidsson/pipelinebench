from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    df = pd.read_csv("seed_data/customer_cdc.csv")
    current = df.drop_duplicates("customer_id", keep="first")
    current[["customer_id", "name", "status"]].to_parquet(
        output_dir / "customer_dimension.parquet",
        index=False,
    )


if __name__ == "__main__":
    main()
