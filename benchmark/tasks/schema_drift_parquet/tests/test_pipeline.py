from __future__ import annotations

from pathlib import Path

import pandas as pd
from starter.pipeline import main


def test_schema_drift_is_preserved_and_normalized() -> None:
    main()

    output = Path("output/accounts.parquet")
    assert output.exists()
    df = pd.read_parquet(output)

    assert list(df.columns) == ["account_id", "balance", "is_active", "opened_at", "account_tier"]
    assert len(df) == 4
    assert df["account_id"].tolist() == [101, 102, 103, 104]
    assert str(df["account_id"].dtype).startswith("int")
    assert str(df["balance"].dtype).startswith("float")
    assert df.loc[df["account_id"] == 103, "account_tier"].iloc[0] == "gold"
    assert df.loc[df["account_id"] == 104, "account_tier"].iloc[0] == "unknown"
    assert df["opened_at"].is_monotonic_increasing
