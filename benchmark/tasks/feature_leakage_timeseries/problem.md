# Time-series feature leakage

The starter ML feature pipeline leaks future target information into rolling features and uses a
random validation split. Fix it so features are generated using only historical values and the
validation split is strictly time based.

Expected outputs:

- `output/features.parquet`
- `output/metrics.json`
