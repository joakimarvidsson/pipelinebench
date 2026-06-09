from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from starter.pipeline import main


def test_features_are_time_safe_and_shape_is_stable() -> None:
    main()

    features = pd.read_parquet("output/features.parquet")
    source = pd.read_csv("seed_data/daily_sales.csv", parse_dates=["date"]).sort_values("date")
    expected = source["sales"].shift(1).rolling(3, min_periods=1).mean()

    assert list(features.columns) == [
        "date",
        "store_id",
        "sales",
        "promo",
        "rolling_sales_3",
        "split",
    ]
    assert len(features) == len(source)
    pd.testing.assert_series_equal(
        features["rolling_sales_3"],
        expected.reset_index(drop=True),
        check_names=False,
    )
    validation_dates = features.loc[
        features["split"] == "validation",
        "date",
    ].dt.strftime("%Y-%m-%d")
    assert validation_dates.tolist() == ["2024-01-08", "2024-01-09", "2024-01-10"]
    assert features.loc[features["split"] == "train", "date"].max() < features.loc[
        features["split"] == "validation", "date"
    ].min()


def test_metrics_are_deterministic_and_not_perfect() -> None:
    main()
    first = json.loads(Path("output/metrics.json").read_text(encoding="utf-8"))
    main()
    second = json.loads(Path("output/metrics.json").read_text(encoding="utf-8"))

    assert first == second
    assert first["validation_rows"] == 3
    assert first["mae_baseline"] > 0
