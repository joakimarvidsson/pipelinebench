from __future__ import annotations

from pathlib import Path

import pandas as pd
from starter.pipeline import main


def test_writes_normalized_customer_parquet() -> None:
    main()

    output = Path("output/customers.parquet")
    assert output.exists()
    df = pd.read_parquet(output)

    assert list(df.columns) == [
        "customer_id",
        "name",
        "signup_date",
        "lifetime_value",
        "email",
    ]
    assert len(df) == 4
    assert df["customer_id"].tolist() == [1, 2, 3, 4]
    assert df["lifetime_value"].round(2).tolist() == [1200.50, 1300.75, 900.00, 2000.00]
    assert pd.isna(df.loc[df["customer_id"] == 4, "signup_date"].iloc[0])
    assert df.loc[df["customer_id"] == 3, "email"].iloc[0] == ""


def test_output_is_deterministic() -> None:
    main()
    first = Path("output/customers.parquet").read_bytes()
    main()
    second = Path("output/customers.parquet").read_bytes()

    assert first == second
