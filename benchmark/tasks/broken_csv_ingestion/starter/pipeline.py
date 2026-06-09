from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    source = Path("seed_data/customers_2024_01.csv")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    df = pd.read_csv(source)
    df.to_parquet(output_dir / "customers.parquet", index=False)


if __name__ == "__main__":
    main()
