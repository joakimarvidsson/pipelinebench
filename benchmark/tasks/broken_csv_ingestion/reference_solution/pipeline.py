from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT_COLUMNS = ["customer_id", "name", "signup_date", "lifetime_value", "email"]


def _normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    normalized.columns = [
        column.strip().lower().replace(" ", "_").replace("-", "_") for column in normalized.columns
    ]
    return normalized


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    frames = [
        _normalize_columns(pd.read_csv(path, dtype=str))
        for path in sorted(Path("seed_data").glob("customers_*.csv"))
    ]
    customers = pd.concat(frames, ignore_index=True)

    customers["customer_id"] = pd.to_numeric(
        customers["customer_id"],
        errors="raise",
    ).astype("int64")
    customers["signup_date"] = pd.to_datetime(
        customers["signup_date"],
        errors="coerce",
        format="mixed",
    )
    customers["lifetime_value"] = (
        customers["lifetime_value"]
        .fillna("0")
        .str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
        .fillna(0.0)
        .astype("float64")
    )
    customers["email"] = customers["email"].fillna("")

    customers = (
        customers.sort_values(["customer_id", "signup_date", "lifetime_value"], na_position="last")
        .drop_duplicates("customer_id", keep="last")
        .sort_values("customer_id")
        .reset_index(drop=True)
    )
    customers[OUTPUT_COLUMNS].to_parquet(output_dir / "customers.parquet", index=False)


if __name__ == "__main__":
    main()
