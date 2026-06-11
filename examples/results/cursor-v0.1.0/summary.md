# Cursor v0.1.0 Baseline Summary

This is an informal local baseline against the five public PipelineBench v0.1.0 tasks. It is not a
hosted leaderboard or a statistically robust model comparison.

| Field | Value |
| --- | --- |
| Tool | Cursor Agent |
| Model | Claude 4.6 Opus |
| Thinking level | High |
| Date | 2026-06-10 AEST |
| Python | 3.14.2 |
| Run repository commit | `2fbd7da` |
| Result | 5/5 tasks passed |

## Results

| Task | Result | Duration | Return code | Tests |
| --- | --- | ---: | ---: | ---: |
| `broken_csv_ingestion` | PASS | 0.604s | 0 | 2 |
| `schema_drift_parquet` | PASS | 0.557s | 0 | 1 |
| `cdc_dedup_scd1` | PASS | 0.565s | 0 | 1 |
| `feature_leakage_timeseries` | PASS | 0.658s | 0 | 2 |
| `duckdb_sql_regression` | PASS | 0.606s | 0 | 1 |

Each evaluation ran `python -m pytest tests`. The preserved result files report all collected tests
passing, empty stderr, and return code `0`.

## Methodology

- Cursor Agent attempted each task in an isolated `.agent-runs/cursor-v0.1.0/` workspace.
- The run was reported as independent from the Codex task solutions.
- Benchmark tests and the PipelineBench harness were not modified.
- Absolute local paths were normalized in the published JSON artifacts.
- The original temporary task workspaces were not retained. This repaired PR validates consistency
  among the per-task JSON, aggregate JSON, leaderboard, and documentation; it does not rerun the
  original Cursor submissions.

Local agent runs can vary with model version, prompt, settings, and environment. PipelineBench
v0.1.0 has public tests only, so this result should be treated as an initial smoke baseline.
