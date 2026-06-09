# Contributing

Thanks for considering a PipelineBench contribution.

Good tasks are realistic, small enough to run locally, and strict enough that passing tests mean the
pipeline failure was genuinely fixed.

Before opening a pull request:

```bash
uv sync
uv run ruff check .
uv run pytest
```

For new benchmark tasks, include:

- `problem.md`
- `task.yaml`
- `seed_data/`
- intentionally broken `starter/`
- validation `tests/`
- maintainer-only `solution_notes.md`

Do not include private data, secrets, paid API calls, or cloud-only validation.
