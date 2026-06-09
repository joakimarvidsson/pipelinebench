# Launch Notes

PipelineBench v0.1.0 is ready for an initial public GitHub launch as a small, inspectable benchmark
for AI agents repairing data engineering and ML pipeline failures.

## Suggested GitHub Metadata

Description:

> An open benchmark for evaluating AI agents on real-world data engineering and ML pipeline failures.

Topics:

```text
ai-agents
benchmark
data-engineering
mlops
duckdb
polars
python
swe-bench
llm-evaluation
pipeline
```

## v0.1.0 Release Notes

PipelineBench v0.1.0 introduces a local, offline benchmark harness for evaluating AI coding agents on
realistic broken data and ML pipelines.

Highlights:

- Python package and CLI: `pipelinebench`
- uv-managed project for Python 3.13 and 3.14
- five bundled benchmark tasks covering CSV ingestion, Parquet schema drift, CDC/SCD1, time-series
  feature leakage, and DuckDB SQL revenue reconciliation
- clean workspace preparation that excludes maintainer-only solution notes
- validation result JSON with command, timing, return code, output tails, and task metadata
- suite runner and Markdown/JSON leaderboard generation
- manual workflow docs for Claude Code, Codex, Cursor, Antigravity, OpenCode, local
  OpenAI-compatible endpoints, and Ollama/Qwen/Kimi-style local model loops
- MIT license and public contribution/security docs

Known limitations:

- starter tasks intentionally fail before an agent repairs them
- no hidden tests yet
- no hosted leaderboard yet
- no security sandbox; validation commands run locally
- no automated proprietary agent control in v0.1

## First Public Push

No remote is required for local use. To publish after creating the GitHub repo:

```bash
git remote add origin git@github.com:joakimarvidsson/pipelinebench.git
git push -u origin codex/pipelinebench-v0.1
```

Then open a pull request into `main`, or rename/merge the branch according to your release workflow.
