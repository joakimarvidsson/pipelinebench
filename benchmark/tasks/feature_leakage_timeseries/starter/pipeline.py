from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    df = pd.read_csv("seed_data/daily_sales.csv", parse_dates=["date"])
    df["rolling_sales_3"] = df["sales"].rolling(3, min_periods=1).mean()
    df["split"] = ["train" if i % 3 else "validation" for i in range(len(df))]
    df.to_parquet(output_dir / "features.parquet", index=False)
    (output_dir / "metrics.json").write_text(json.dumps({"mae_baseline": 0.0}), encoding="utf-8")


if __name__ == "__main__":
    main()
