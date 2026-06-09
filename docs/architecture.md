# Architecture

PipelineBench v0.1 has four layers:

1. Task metadata and files under `benchmark/tasks/<task_id>/`.
2. A typed Python harness in `src/pipelinebench`.
3. A Typer/Rich CLI exposed as `pipelinebench`.
4. Local JSON and Markdown artifacts for result reporting.

The harness deliberately avoids cloud credentials, paid APIs, and proprietary agent automation. It
copies a task into a workspace, excludes maintainer-only notes, runs the validation command from the
workspace root, and records a serializable result.

## Modules

- `schema.py` defines Pydantic models for task metadata and validation results.
- `tasks.py` discovers and validates task definitions.
- `workspace.py` prepares local agent workspaces.
- `runner.py` executes validation commands and writes result JSON.
- `leaderboard.py` renders Markdown and JSON summaries.
- `adapters.py` documents manual agent workflows.
- `cli.py` wires the harness into a demoable command-line interface.

## Non-goals in v0.1

- No hidden tests.
- No remote execution.
- No unsafe isolation claims.
- No automated proprietary agent control.
- No public hosted leaderboard service.
