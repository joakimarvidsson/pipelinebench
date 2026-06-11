# Baseline Results

Baseline results are example runs for orientation. They are not a formal leaderboard, and they should
not be treated as a statistically meaningful model comparison.

## Comparison Summary

| Baseline | Tool | Model / settings | Tasks passed | Pass rate | Artifact path |
| --- | --- | --- | ---: | ---: | --- |
| Codex v0.1.0 | Codex | Model not reported, high reasoning | 5/5 | 100% | `examples/results/codex-v0.1.0/` |
| Cursor v0.1.0 | Cursor Agent | Claude 4.6 Opus, high thinking | 5/5 | 100% | `examples/results/cursor-v0.1.0/` |

Both entries are single local runs against the same public v0.1.0 task pack. They are useful for
orientation, not for ranking models or agents. Runtime differences at this scale are environment
noise rather than meaningful performance comparisons.

## Codex v0.1.0 Baseline

| Field | Value |
| --- | --- |
| Tool | Codex |
| Model | Codex, model not reported by CLI/UI |
| Reasoning level | High |
| Date | 2026-06-11 AEST |
| PipelineBench version | v0.1.0 |
| PipelineBench commit | `a46162f` |
| Python | 3.14.2 |
| Public artifact path | `examples/results/codex-v0.1.0/` |
| Formal leaderboard? | No |

### Results

| Task | Result | Tests | Duration |
| --- | --- | ---: | ---: |
| `broken_csv_ingestion` | PASS | 2 | 0.591s |
| `schema_drift_parquet` | PASS | 1 | 0.547s |
| `cdc_dedup_scd1` | PASS | 1 | 0.495s |
| `feature_leakage_timeseries` | PASS | 2 | 0.500s |
| `duckdb_sql_regression` | PASS | 1 | 0.505s |

Summary: 5/5 tasks passed under the public v0.1.0 tests.

### Commands Used

```bash
git switch -c baseline/codex-v0.1.0

rm -rf .agent-runs/codex-v0.1.0
mkdir -p .agent-runs/codex-v0.1.0/results

for task in broken_csv_ingestion schema_drift_parquet cdc_dedup_scd1 feature_leakage_timeseries duckdb_sql_regression; do
  uv run --python 3.14 pipelinebench run-task "$task" \
    --workspace ".agent-runs/codex-v0.1.0/$task"
done

for task in broken_csv_ingestion schema_drift_parquet cdc_dedup_scd1 feature_leakage_timeseries duckdb_sql_regression; do
  uv run --python 3.14 pipelinebench evaluate "$task" \
    --submission ".agent-runs/codex-v0.1.0/$task" \
    --output ".agent-runs/codex-v0.1.0/results/${task}.json"
done

uv run --python 3.14 pipelinebench leaderboard \
  --results examples/results/codex-v0.1.0/results.json \
  --output-prefix examples/results/codex-v0.1.0/leaderboard
```

The published JSON under `examples/results/codex-v0.1.0/` normalizes local absolute workspace paths
to repo-relative paths. The pass/fail status, durations, commands, return codes, output tails, and
task metadata are copied from the actual local evaluation result JSON.

### Limitations

- This baseline used public tests only; PipelineBench v0.1.0 has no hidden split.
- This is a single local run, not a repeated or statistically robust evaluation.
- The task workspaces were fixed manually by Codex in this repository session, not by an automated
  standardized agent runner.
- Codex did not read maintainer solution notes or reference solutions, and changed only each
  generated workspace's `starter/pipeline.py`.
- Local agent runs may vary by model version, prompt, settings, and environment.
- Results are useful as an initial smoke baseline, not as a formal public ranking.

## Cursor v0.1.0 Baseline

| Field | Value |
| --- | --- |
| Tool | Cursor Agent |
| Model | Claude 4.6 Opus |
| Thinking level | High |
| Date | 2026-06-10 AEST |
| PipelineBench version | v0.1.0 |
| Run repository commit | `2fbd7da` |
| Python | 3.14.2 |
| Public artifact path | `examples/results/cursor-v0.1.0/` |
| Formal leaderboard? | No |

### Results

| Task | Result | Tests | Duration |
| --- | --- | ---: | ---: |
| `broken_csv_ingestion` | PASS | 2 | 0.604s |
| `schema_drift_parquet` | PASS | 1 | 0.557s |
| `cdc_dedup_scd1` | PASS | 1 | 0.565s |
| `feature_leakage_timeseries` | PASS | 2 | 0.658s |
| `duckdb_sql_regression` | PASS | 1 | 0.606s |

Summary: 5/5 tasks passed under the public v0.1.0 tests.

### Commands Used

```bash
uv run --python 3.14 pipelinebench run-task TASK_ID \
  --workspace .agent-runs/cursor-v0.1.0/TASK_ID

uv run --python 3.14 pipelinebench evaluate TASK_ID \
  --submission .agent-runs/cursor-v0.1.0/TASK_ID \
  --output .agent-runs/cursor-v0.1.0/results/TASK_ID.json

uv run --python 3.14 pipelinebench leaderboard \
  --results examples/results/cursor-v0.1.0/results.json \
  --output-prefix examples/results/cursor-v0.1.0/leaderboard
```

### Limitations

- This baseline used public tests only; PipelineBench v0.1.0 has no hidden split.
- This is a single local run, not a repeated or statistically robust evaluation.
- The original temporary Cursor task workspaces were not retained in the public branch. This PR
  repair verifies consistency among the preserved result files but does not rerun those submissions.
- Local agent runs may vary by model version, prompt, settings, and environment.
- Results are useful as an initial smoke baseline, not as a formal public ranking.
