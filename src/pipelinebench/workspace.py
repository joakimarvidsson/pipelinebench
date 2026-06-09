from __future__ import annotations

import shutil
from pathlib import Path

from pipelinebench.schema import TaskSpec

WORKSPACE_ITEMS = ("problem.md", "task.yaml", "seed_data", "starter", "tests")


def prepare_workspace(task: TaskSpec, workspace: Path) -> Path:
    """Create a clean local workspace for an agent attempt."""

    if task.task_dir is None:
        msg = f"Task '{task.id}' has no task_dir; load it through pipelinebench.tasks"
        raise ValueError(msg)

    workspace = workspace.resolve()
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    for item in WORKSPACE_ITEMS:
        source = task.task_dir / item
        destination = workspace / item
        if source.is_dir():
            shutil.copytree(source, destination)
        elif source.is_file():
            shutil.copy2(source, destination)
        else:
            msg = f"Task '{task.id}' is missing required item: {item}"
            raise FileNotFoundError(msg)

    return workspace
