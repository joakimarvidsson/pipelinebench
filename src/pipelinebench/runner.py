from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

from pipelinebench.schema import TaskSpec, ValidationResult, utc_now_iso
from pipelinebench.tasks import discover_tasks
from pipelinebench.workspace import prepare_workspace

TAIL_CHARS = 4000


def run_validation(task: TaskSpec, workspace: Path, command: str | None = None) -> ValidationResult:
    """Run a task validation command from a workspace root."""

    workspace = workspace.resolve()
    command = command or task.validation_command
    started_at = utc_now_iso()
    monotonic_start = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=workspace,
        shell=True,
        text=True,
        capture_output=True,
        check=False,
    )
    finished_at = utc_now_iso()
    duration = time.perf_counter() - monotonic_start
    stdout_tail = completed.stdout[-TAIL_CHARS:]
    stderr_tail = completed.stderr[-TAIL_CHARS:]

    return ValidationResult(
        task_id=task.id,
        title=task.title,
        category=task.category,
        difficulty=task.difficulty,
        passed=completed.returncode == 0,
        duration_seconds=round(duration, 3),
        command=command,
        return_code=completed.returncode,
        stdout_tail=stdout_tail,
        stderr_tail=stderr_tail,
        started_at=started_at,
        finished_at=finished_at,
        workspace_path=str(workspace),
        test_count=parse_pytest_count(stdout_tail + "\n" + stderr_tail),
        error_summary=summarize_error(stdout_tail, stderr_tail, completed.returncode),
    )


def run_suite(workspace_root: Path, output_path: Path | None = None) -> list[ValidationResult]:
    """Prepare and validate every discovered task."""

    results: list[ValidationResult] = []
    for task in discover_tasks():
        workspace = prepare_workspace(task, workspace_root / task.id)
        results.append(run_validation(task=task, workspace=workspace))

    if output_path is not None:
        write_results(results, output_path)
    return results


def write_results(results: list[ValidationResult], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([result.model_dump(mode="json") for result in results], indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def parse_pytest_count(output: str) -> int | None:
    matches = re.findall(r"(\d+)\s+(?:passed|failed|error|errors|skipped|xfailed|xpassed)", output)
    if not matches:
        return None
    return sum(int(match) for match in matches)


def summarize_error(stdout_tail: str, stderr_tail: str, return_code: int) -> str:
    if return_code == 0:
        return ""
    combined = "\n".join(part for part in (stdout_tail, stderr_tail) if part).strip()
    if not combined:
        return f"Validation command failed with return code {return_code}"
    lines = [line.strip() for line in combined.splitlines() if line.strip()]
    interesting = [
        line
        for line in lines
        if "FAILED" in line or "ERROR" in line or "AssertionError" in line or "E   " in line
    ]
    return (interesting[0] if interesting else lines[-1])[:500]
