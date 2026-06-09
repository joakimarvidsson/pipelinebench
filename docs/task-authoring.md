# Task Authoring

Create a task scaffold:

```bash
uv run pipelinebench new-task my_task_id
```

Each task must contain:

```text
problem.md
task.yaml
seed_data/
starter/
tests/
solution_notes.md
```

`task.yaml` is validated with Pydantic. Keep the id identical to the directory name.

```yaml
id: broken_csv_ingestion
title: Broken CSV ingestion
category: ingestion
difficulty: easy
skills:
  - csv
  - parquet
entrypoint: starter/pipeline.py
expected_outputs:
  - output/customers.parquet
time_budget_minutes: 20
allowed_files:
  - starter/**
  - seed_data/**
validation_command: python -m pytest tests
scoring:
  type: pytest
  pass_threshold: 1.0
```

Good tasks have:

- realistic broken starter code
- small, inspectable seed data
- clear public tests
- deterministic outputs
- maintainer notes that explain the intended fix

Do not include private data, secrets, external credentials, or required network access.
