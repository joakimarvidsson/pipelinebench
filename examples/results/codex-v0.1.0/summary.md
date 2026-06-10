# Codex v0.1.0 Baseline Summary

This is an informal local baseline against the five public PipelineBench v0.1.0 tasks. It is not a
hosted leaderboard or a statistically robust model comparison.

| Field | Value |
| --- | --- |
| Tool | Codex |
| Model | Codex, model not reported by CLI/UI |
| Reasoning level | High |
| Date | 2026-06-11 AEST |
| Python | 3.14.2 |
| PipelineBench commit | `a46162f` |
| Result | 5/5 tasks passed |

## Results

| Task | Result | Duration | Return code | Tests | Workspace file edited |
| --- | --- | ---: | ---: | ---: | --- |
| `broken_csv_ingestion` | PASS | 0.591s | 0 | 2 | `starter/pipeline.py` |
| `schema_drift_parquet` | PASS | 0.547s | 0 | 1 | `starter/pipeline.py` |
| `cdc_dedup_scd1` | PASS | 0.495s | 0 | 1 | `starter/pipeline.py` |
| `feature_leakage_timeseries` | PASS | 0.500s | 0 | 2 | `starter/pipeline.py` |
| `duckdb_sql_regression` | PASS | 0.505s | 0 | 1 | `starter/pipeline.py` |

Each evaluation ran `python -m pytest tests`. Stdout showed all collected tests passing, stderr was
empty, and each command returned `0`. The per-task JSON files preserve the concise output tails.

## Commands

Each workspace was created with:

```bash
uv run --python 3.14 pipelinebench run-task TASK_ID \
  --workspace .agent-runs/codex-v0.1.0/TASK_ID
```

Each completed submission was evaluated with:

```bash
uv run --python 3.14 pipelinebench evaluate TASK_ID \
  --submission .agent-runs/codex-v0.1.0/TASK_ID \
  --output .agent-runs/codex-v0.1.0/results/TASK_ID.json
```

The aggregate leaderboard was generated with:

```bash
uv run --python 3.14 pipelinebench leaderboard \
  --results examples/results/codex-v0.1.0/results.json \
  --output-prefix examples/results/codex-v0.1.0/leaderboard
```

## Methodology

- Codex attempted each task in a fresh isolated workspace.
- Only the generated workspace `starter/pipeline.py` was edited for each task.
- Benchmark tests and the PipelineBench harness were not modified.
- Maintainer `solution_notes.md` and reference solutions were not used.
- The fixes were completed independently from the problem statement, seed data, starter code, and
  public tests copied into each task workspace.
- Absolute local paths were normalized in the published JSON artifacts.

Local agent runs can vary with model version, prompt, settings, and environment. PipelineBench
v0.1.0 has public tests only, so this result should be treated as an initial smoke baseline.
