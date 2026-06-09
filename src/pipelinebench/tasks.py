from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from pipelinebench.schema import TaskSpec

DEFAULT_TASKS_DIR = Path(__file__).resolve().parents[2] / "benchmark" / "tasks"


class TaskLoadError(ValueError):
    """Raised when a task cannot be loaded or validated."""


def discover_tasks(tasks_dir: Path = DEFAULT_TASKS_DIR) -> list[TaskSpec]:
    """Discover benchmark tasks from a benchmark/tasks directory."""

    if not tasks_dir.exists():
        return []

    tasks: list[TaskSpec] = []
    for task_yaml in sorted(tasks_dir.glob("*/task.yaml")):
        tasks.append(load_task_from_path(task_yaml))
    return tasks


def load_task(task_id: str, tasks_dir: Path = DEFAULT_TASKS_DIR) -> TaskSpec:
    """Load one task by id."""

    task_yaml = tasks_dir / task_id / "task.yaml"
    if not task_yaml.exists():
        msg = f"Task '{task_id}' was not found under {tasks_dir}"
        raise TaskLoadError(msg)
    return load_task_from_path(task_yaml)


def load_task_from_path(task_yaml: Path) -> TaskSpec:
    """Load and validate a task.yaml file."""

    try:
        payload = yaml.safe_load(task_yaml.read_text(encoding="utf-8")) or {}
        task = TaskSpec.model_validate(payload)
    except ValidationError as exc:
        msg = f"Invalid task metadata in {task_yaml}:\n{exc}"
        raise TaskLoadError(msg) from exc
    except yaml.YAMLError as exc:
        msg = f"Invalid YAML in {task_yaml}: {exc}"
        raise TaskLoadError(msg) from exc

    if task.id != task_yaml.parent.name:
        msg = f"Task id '{task.id}' must match directory name '{task_yaml.parent.name}'"
        raise TaskLoadError(msg)

    task.task_dir = task_yaml.parent
    return task
