from __future__ import annotations

from pathlib import Path

import pandas as pd
from starter.pipeline import main


def test_current_state_uses_latest_non_deleted_events() -> None:
    main()

    output = Path("output/customer_dimension.parquet")
    assert output.exists()
    df = pd.read_parquet(output)

    assert list(df.columns) == ["customer_id", "name", "status"]
    assert df["customer_id"].tolist() == [1, 3]
    assert df["customer_id"].is_unique
    assert df.loc[df["customer_id"] == 1, "status"].iloc[0] == "silver"
    assert df.loc[df["customer_id"] == 3, "name"].iloc[0] == "Charlie"
    assert df.loc[df["customer_id"] == 3, "status"].iloc[0] == "gold"
