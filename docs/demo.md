# Demo

This demo shows the intended starter-task failure before an agent repairs the pipeline.

```bash
uv sync
uv run pipelinebench list-tasks
uv run pipelinebench run-task broken_csv_ingestion --workspace .workspaces/broken_csv_ingestion
```

Expected shape:

```text
PipelineBench Tasks
broken_csv_ingestion  Broken CSV ingestion  ingestion  easy  csv, parquet, ...

FAIL broken_csv_ingestion in 1.234s
Command: python -m pytest tests
Return code: 1
Result JSON: .workspaces/broken_csv_ingestion/.pipelinebench-result.json
```

Now open `.workspaces/broken_csv_ingestion` in Claude Code, Codex, Cursor, Antigravity, OpenCode, or
your local model workflow. Give the agent `problem.md` and ask it to make this command pass:

```bash
python -m pytest tests
```

After the agent edits the workspace:

```bash
uv run pipelinebench evaluate broken_csv_ingestion --submission .workspaces/broken_csv_ingestion
```

For a suite run:

```bash
uv run pipelinebench run-suite --workspace .workspaces/suite --output results/pipelinebench-results.json
uv run pipelinebench leaderboard --results results/pipelinebench-results.json --output-prefix results/leaderboard
```

Do not fake successful benchmark results. Starter tasks are expected to fail before repair.
