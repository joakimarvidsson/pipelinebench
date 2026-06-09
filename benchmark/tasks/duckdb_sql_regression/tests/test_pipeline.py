from __future__ import annotations

from pathlib import Path

import pandas as pd
from starter.pipeline import main


def test_revenue_reconciles_and_join_cardinality_is_controlled() -> None:
    main()

    output = Path("output/order_revenue.parquet")
    assert output.exists()
    df = pd.read_parquet(output)
    orders = pd.read_csv("seed_data/orders.csv")

    assert len(df) == len(orders)
    assert df["order_id"].is_unique
    assert round(df["revenue"].sum(), 2) == round(orders["revenue"].sum(), 2)
    assert df["order_id"].tolist() == [1001, 1002, 1003, 1004]
    assert df.loc[df["order_id"] == 1001, "channel"].iloc[0] == "email"
    assert df.loc[df["order_id"] == 1004, "channel"].isna().iloc[0]
