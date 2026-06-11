# PipelineBench

**An open benchmark for evaluating AI agents on real-world data engineering failures.**

**Can your AI agent fix a broken data pipeline?**

[![Python](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

PipelineBench is a local, reproducible benchmark and reference harness for testing whether AI
coding agents can repair realistic data engineering and ML pipeline failures. It is benchmark-first,
agent-agnostic, offline by default, and built around strong task tests with visible leaderboard
output.

> v0.1 is intentionally small: five broken pipelines, a clean CLI, local workspaces, JSON results,
> and Markdown leaderboard output.

## Quickstart

```bash
uv sync
uv run pipelinebench --version
uv run pipelinebench list-tasks
uv run pipelinebench run-task broken_csv_ingestion --workspace .workspaces/broken_csv_ingestion
uv run pipelinebench evaluate broken_csv_ingestion --submission .workspaces/broken_csv_ingestion
```

The starter task should fail before an agent fixes it. That failure is the benchmark prompt, not a
setup error.

## Why this exists

AI coding agents are increasingly evaluated on general software tasks, but data engineering work has
its own failure modes: schema drift, CDC ordering, SQL join regressions, data quality contracts,
time-series leakage, and reproducible outputs. PipelineBench gives teams a concrete way to test those
skills locally without cloud accounts, paid APIs, or private data.

## What PipelineBench measures

- Can an agent understand a broken data or ML pipeline from tests and task context?
- Can it preserve data contracts while handling messy inputs?
- Can it avoid silent data loss, leakage, duplicate records, and nondeterministic outputs?
- Can it produce a passing, reproducible local result under realistic constraints?

## How tasks work

Each task lives under `benchmark/tasks/<task_id>/`:

```text
problem.md
task.yaml
seed_data/
starter/
tests/
solution_notes.md
```

`solution_notes.md` is maintainer-only and is not copied into agent workspaces by default.

## How to compare agents

1. Prepare a task workspace.
2. Open that workspace in the agent tool.
3. Give the agent `problem.md` and ask it to make `python -m pytest tests` pass.
4. Evaluate the resulting workspace.
5. Save result JSON.
6. Generate a leaderboard.

```bash
uv run pipelinebench run-task broken_csv_ingestion --workspace .workspaces/broken_csv_ingestion
uv run pipelinebench evaluate broken_csv_ingestion --submission .workspaces/broken_csv_ingestion
uv run pipelinebench run-suite --workspace .workspaces/suite --output results/pipelinebench-results.json
uv run pipelinebench leaderboard --results results/pipelinebench-results.json
```

Do not report starter failures as successful benchmark results.

## Run a Task

```bash
uv run pipelinebench run-task broken_csv_ingestion --workspace .workspaces/broken_csv_ingestion
```

This creates a clean local workspace containing `problem.md`, `task.yaml`, `seed_data/`, `starter/`,
and `tests/`. Maintainer-only notes are excluded.

## Evaluate an Agent

After an agent edits the workspace:

```bash
uv run pipelinebench evaluate broken_csv_ingestion --submission .workspaces/broken_csv_ingestion
```

The command writes `.pipelinebench-result.json` by default inside the submission workspace.

## Generate a Leaderboard

```bash
uv run pipelinebench run-suite --workspace .workspaces/suite --output results/pipelinebench-results.json
uv run pipelinebench leaderboard --results results/pipelinebench-results.json --output-prefix results/leaderboard
```

The leaderboard command writes readable Markdown and machine-readable JSON.

## Baseline Results

Informal Codex and Cursor Agent smoke baselines are available in
[docs/baselines.md](docs/baselines.md), with public artifacts under
[examples/results](examples/results). They record single local runs against the v0.1.0 public tests
and are not a formal hosted leaderboard.

## Supported agent workflows

PipelineBench v0.1 does not automate proprietary tools. It prepares local workspaces that can be
opened manually in:

- Claude Code
- Codex
- Cursor
- Antigravity
- OpenCode
- local OpenAI-compatible agent runners
- Ollama/Qwen/Kimi-style local model workflows

See [docs/agent-runners.md](docs/agent-runners.md).

## Initial benchmark tasks

| Task | Category | Difficulty | Focus |
| --- | --- | --- | --- |
| `broken_csv_ingestion` | ingestion | easy | messy CSV normalization and Parquet output |
| `schema_drift_parquet` | ingestion | medium | schema evolution and stable output contracts |
| `cdc_dedup_scd1` | cdc | medium | CDC deduplication and SCD1 current state |
| `feature_leakage_timeseries` | ml | medium | time-safe feature generation and validation split |
| `duckdb_sql_regression` | sql | medium | DuckDB join cardinality and revenue reconciliation |

## CLI

```bash
pipelinebench --version
pipelinebench list-tasks
pipelinebench run-task TASK_ID --workspace PATH
pipelinebench evaluate TASK_ID --submission PATH
pipelinebench run-suite --workspace PATH
pipelinebench leaderboard --results PATH
pipelinebench new-task TASK_ID
```

## Contributing new tasks

Start with:

```bash
uv run pipelinebench new-task my_pipeline_failure
```

Then add realistic seed data, intentionally broken starter code, clear tests, and maintainer notes.
See [docs/task-authoring.md](docs/task-authoring.md).

## Security / sandboxing note

PipelineBench v0.1 is local and offline by default, but it is not a security sandbox. Validation
commands execute on your machine in the selected workspace. Review third-party tasks before running
them and use your own OS/container isolation if you need stronger boundaries.

## Launch Status

PipelineBench v0.1.0 is ready for a first public GitHub launch:

- five bundled starter-failing tasks
- one maintainer reference solution validated in tests
- local JSON result artifacts
- Markdown and JSON leaderboard output
- CI configured for Python 3.13 and 3.14

Suggested GitHub description:

> An open benchmark for evaluating AI agents on real-world data engineering and ML pipeline failures.

Suggested topics:

`ai-agents`, `benchmark`, `data-engineering`, `mlops`, `duckdb`, `polars`, `python`, `swe-bench`,
`llm-evaluation`, `pipeline`

## Roadmap

Planned v0.2 directions:

- dbt tasks
- Spark tasks
- Great Expectations tasks
- Soda data quality tasks
- MLflow tasks
- Airflow/Dagster/Prefect DAG tasks
- hidden test split support
- public leaderboard GitHub Action
- MCP server integration
- FastAPI dashboard
- local Qwen/Kimi/Ollama reference agent
- synthetic enterprise warehouse tasks
- Databricks-style medallion pipeline tasks
- Python 3.15 official support after Python 3.15 final release and dependency validation

## License

MIT. See [LICENSE](LICENSE).
