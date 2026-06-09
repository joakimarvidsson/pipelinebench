from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from pipelinebench import __version__
from pipelinebench.leaderboard import build_leaderboard, write_leaderboard
from pipelinebench.runner import run_suite as run_suite_impl
from pipelinebench.runner import run_validation, write_results
from pipelinebench.schema import ValidationResult
from pipelinebench.tasks import TaskLoadError, discover_tasks, load_task
from pipelinebench.workspace import prepare_workspace

app = typer.Typer(
    name="pipelinebench",
    help="PipelineBench: an open benchmark for realistic data/ML pipeline failures.",
    no_args_is_help=True,
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"pipelinebench {__version__}")
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the PipelineBench version.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    _ = version


@app.command("list-tasks")
def list_tasks() -> None:
    """List bundled benchmark tasks."""

    table = Table(title="PipelineBench Tasks")
    table.add_column("Task ID", style="cyan", no_wrap=True)
    table.add_column("Title")
    table.add_column("Category")
    table.add_column("Difficulty")
    table.add_column("Skills")
    for task in discover_tasks():
        table.add_row(task.id, task.title, task.category, task.difficulty, ", ".join(task.skills))
    console.print(table)


@app.command("run-task")
def run_task(
    task_id: Annotated[str, typer.Argument(help="Benchmark task id.")],
    workspace: Annotated[Path, typer.Option("--workspace", "-w", help="Workspace path.")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Optional result JSON path."),
    ] = None,
) -> None:
    """Prepare a clean task workspace and run its validation command."""

    task = _load_task_or_exit(task_id)
    prepared = prepare_workspace(task, workspace)
    result = run_validation(task=task, workspace=prepared)
    output_path = output or prepared / ".pipelinebench-result.json"
    write_results([result], output_path)
    _print_result(result, output_path)


@app.command("evaluate")
def evaluate(
    task_id: Annotated[str, typer.Argument(help="Benchmark task id.")],
    submission: Annotated[
        Path,
        typer.Option("--submission", "-s", help="Submission/workspace path."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Optional result JSON path."),
    ] = None,
) -> None:
    """Run validation against an existing submission workspace."""

    task = _load_task_or_exit(task_id)
    result = run_validation(task=task, workspace=submission)
    output_path = output or submission / ".pipelinebench-result.json"
    write_results([result], output_path)
    _print_result(result, output_path)


@app.command("run-suite")
def run_suite(
    workspace: Annotated[Path, typer.Option("--workspace", "-w", help="Suite workspace root.")],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Aggregate result JSON path."),
    ] = Path("pipelinebench-results.json"),
) -> None:
    """Prepare and validate all bundled tasks."""

    results = run_suite_impl(workspace_root=workspace, output_path=output)
    passed = sum(1 for result in results if result.passed)
    console.print(f"[bold]Suite complete:[/] {passed}/{len(results)} tasks passed")
    console.print(f"Results: {output}")


@app.command("leaderboard")
def leaderboard(
    results: Annotated[Path, typer.Option("--results", "-r", help="Result JSON from run-suite.")],
    output_prefix: Annotated[
        Path,
        typer.Option("--output-prefix", "-o", help="Leaderboard output prefix."),
    ] = Path("pipelinebench-leaderboard"),
) -> None:
    """Generate Markdown and JSON leaderboard artifacts."""

    payload = json.loads(results.read_text(encoding="utf-8"))
    leaderboard_output = build_leaderboard(payload)
    markdown_path, json_path = write_leaderboard(leaderboard_output, output_prefix)
    console.print(leaderboard_output.markdown)
    console.print(f"Markdown: {markdown_path}")
    console.print(f"JSON: {json_path}")


@app.command("new-task")
def new_task(task_id: Annotated[str, typer.Argument(help="New task id.")]) -> None:
    """Scaffold a new benchmark task directory."""

    target = Path("benchmark") / "tasks" / task_id
    if target.exists():
        console.print(f"[red]Task already exists:[/] {target}")
        raise typer.Exit(1)

    for child in ("seed_data", "starter", "tests"):
        (target / child).mkdir(parents=True, exist_ok=True)
    (target / "problem.md").write_text(
        f"# {task_id}\n\nDescribe the broken pipeline.\n",
        encoding="utf-8",
    )
    (target / "solution_notes.md").write_text(
        "# Maintainer solution notes\n\nDo not copy this file into agent workspaces.\n",
        encoding="utf-8",
    )
    (target / "starter" / "pipeline.py").write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "",
                "",
                "def main() -> None:",
                "    Path('output').mkdir(exist_ok=True)",
                "",
                "",
                "if __name__ == '__main__':",
                "    main()",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (target / "tests" / "test_pipeline.py").write_text(
        "def test_pipeline_contract() -> None:\n    assert False, 'write task validation tests'\n",
        encoding="utf-8",
    )
    (target / "task.yaml").write_text(
        "\n".join(
            [
                f"id: {task_id}",
                f"title: {task_id.replace('_', ' ').title()}",
                "category: ingestion",
                "difficulty: easy",
                "skills:",
                "  - data-quality",
                "entrypoint: starter/pipeline.py",
                "expected_outputs:",
                "  - output/result.parquet",
                "time_budget_minutes: 20",
                "allowed_files:",
                "  - starter/**",
                "  - seed_data/**",
                "validation_command: python -m pytest tests",
                "scoring:",
                "  type: pytest",
                "  pass_threshold: 1.0",
                "",
            ]
        ),
        encoding="utf-8",
    )
    console.print(f"Created {target}")


def _load_task_or_exit(task_id: str):
    try:
        return load_task(task_id)
    except TaskLoadError as exc:
        console.print(f"[red]{exc}[/]")
        raise typer.Exit(1) from exc


def _print_result(result: ValidationResult, output_path: Path) -> None:
    status = "[green]PASS[/]" if result.passed else "[red]FAIL[/]"
    console.print(f"{status} {result.task_id} in {result.duration_seconds:.3f}s")
    console.print(f"Command: {result.command}")
    console.print(f"Return code: {result.return_code}")
    console.print(f"Result JSON: {output_path}")
    if result.error_summary:
        console.print(f"Error summary: {result.error_summary}")
