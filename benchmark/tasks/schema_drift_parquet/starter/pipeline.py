from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    df = pd.read_parquet("seed_data/accounts_day_1.parquet")
    df.to_parquet(output_dir / "accounts.parquet", index=False)


if __name__ == "__main__":
    main()
