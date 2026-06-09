from __future__ import annotations

import json
import shutil
from pathlib import Path

from typer.testing import CliRunner

from pipelinebench.cli import app
from pipelinebench.leaderboard import build_leaderboard, write_leaderboard
from pipelinebench.runner import run_validation
from pipelinebench.tasks import discover_tasks, load_task
from pipelinebench.workspace import prepare_workspace


def test_discovers_initial_tasks() -> None:
    tasks = discover_tasks()
    task_ids = [task.id for task in tasks]

    assert len(tasks) == 5
    assert sorted(task_ids) == sorted(
        {
            "broken_csv_ingestion",
            "schema_drift_parquet",
            "cdc_dedup_scd1",
            "feature_leakage_timeseries",
            "duckdb_sql_regression",
        }
    )
    assert len(task_ids) == len(set(task_ids))
    for task in tasks:
        assert task.task_dir is not None
        assert (task.task_dir / "problem.md").exists()
        assert (task.task_dir / "solution_notes.md").exists()
        assert task.entrypoint.startswith("starter/")
        assert task.expected_outputs
        assert task.validation_command == "python -m pytest tests"


def test_all_workspace_contract_files_are_copied(tmp_path: Path) -> None:
    task = load_task("schema_drift_parquet")
    workspace = prepare_workspace(task, tmp_path / "workspace")

    expected_items = {
        "problem.md",
        "task.yaml",
        "seed_data",
        "starter",
        "tests",
    }

    assert expected_items.issubset({path.name for path in workspace.iterdir()})
    assert (workspace / "seed_data" / "accounts_day_1.parquet").exists()
    assert (workspace / "seed_data" / "accounts_day_2.parquet").exists()
    assert not (workspace / "solution_notes.md").exists()
    assert not (workspace / "reference_solution").exists()


def test_cli_run_task_writes_required_result_fields(tmp_path: Path) -> None:
    runner = CliRunner()
    workspace = tmp_path / "broken_csv_ingestion"
    output = tmp_path / "result.json"

    result = runner.invoke(
        app,
        [
            "run-task",
            "broken_csv_ingestion",
            "--workspace",
            str(workspace),
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert len(payload) == 1
    required_fields = {
        "task_id",
        "title",
        "category",
        "difficulty",
        "passed",
        "duration_seconds",
        "command",
        "return_code",
        "stdout_tail",
        "stderr_tail",
        "started_at",
        "finished_at",
        "workspace_path",
        "test_count",
        "error_summary",
    }
    assert required_fields.issubset(payload[0])
    assert payload[0]["task_id"] == "broken_csv_ingestion"
    assert payload[0]["passed"] is False
    assert payload[0]["return_code"] != 0


def test_write_leaderboard_generates_markdown_and_json_files(tmp_path: Path) -> None:
    leaderboard = build_leaderboard(
        [
            {
                "task_id": "broken_csv_ingestion",
                "title": "Broken CSV ingestion",
                "category": "ingestion",
                "difficulty": "easy",
                "passed": False,
                "duration_seconds": 0.5,
                "command": "python -m pytest tests",
                "return_code": 1,
                "stdout_tail": "1 failed",
                "stderr_tail": "",
                "started_at": "2026-01-01T00:00:00Z",
                "finished_at": "2026-01-01T00:00:01Z",
                "workspace_path": "/tmp/workspace",
                "test_count": 1,
                "error_summary": "failed",
            }
        ]
    )

    markdown_path, json_path = write_leaderboard(leaderboard, tmp_path / "leaderboard")

    assert markdown_path.read_text(encoding="utf-8").startswith("# PipelineBench Leaderboard")
    summary = json.loads(json_path.read_text(encoding="utf-8"))
    assert summary["total_tasks"] == 1
    assert summary["passed_tasks"] == 0


def test_reference_solution_for_csv_task_passes_validation(tmp_path: Path) -> None:
    task = load_task("broken_csv_ingestion")
    assert task.task_dir is not None
    workspace = prepare_workspace(task, tmp_path / "broken_csv_ingestion")
    shutil.copy2(
        task.task_dir / "reference_solution" / "pipeline.py",
        workspace / "starter" / "pipeline.py",
    )

    result = run_validation(task=task, workspace=workspace, command=task.validation_command)

    assert result.passed is True
    assert result.return_code == 0
    assert result.test_count == 2


def test_cli_help_for_required_commands() -> None:
    runner = CliRunner()
    commands = [
        "list-tasks",
        "run-task",
        "evaluate",
        "run-suite",
        "leaderboard",
        "new-task",
    ]

    for command in commands:
        result = runner.invoke(app, [command, "--help"])

        assert result.exit_code == 0
        assert command in result.output


def test_loads_task_schema() -> None:
    task = load_task("broken_csv_ingestion")

    assert task.id == "broken_csv_ingestion"
    assert task.validation_command == "python -m pytest tests"
    assert task.scoring.type == "pytest"
    assert task.scoring.pass_threshold == 1.0


def test_prepare_workspace_excludes_solution_notes(tmp_path: Path) -> None:
    task = load_task("broken_csv_ingestion")
    workspace = prepare_workspace(task, tmp_path / "workspace")

    assert (workspace / "problem.md").exists()
    assert (workspace / "task.yaml").exists()
    assert (workspace / "seed_data").is_dir()
    assert (workspace / "starter").is_dir()
    assert (workspace / "tests").is_dir()
    assert not (workspace / "solution_notes.md").exists()


def test_run_validation_records_json_serializable_result(tmp_path: Path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_sample.py").write_text(
        "def test_sample():\n    assert True\n",
        encoding="utf-8",
    )

    result = run_validation(
        task=load_task("broken_csv_ingestion"),
        workspace=tmp_path,
        command="python -m pytest tests",
    )

    assert result.passed is True
    assert result.return_code == 0
    assert result.test_count >= 1
    json.loads(result.model_dump_json())


def test_leaderboard_generates_markdown_and_summary() -> None:
    payload = [
        {
            "task_id": "a",
            "title": "Task A",
            "category": "ingestion",
            "difficulty": "easy",
            "passed": True,
            "duration_seconds": 1.2,
            "command": "python -m pytest tests",
            "return_code": 0,
            "stdout_tail": "1 passed",
            "stderr_tail": "",
            "started_at": "2026-01-01T00:00:00Z",
            "finished_at": "2026-01-01T00:00:01Z",
            "workspace_path": "/tmp/a",
            "test_count": 1,
            "error_summary": "",
        },
        {
            "task_id": "b",
            "title": "Task B",
            "category": "sql",
            "difficulty": "medium",
            "passed": False,
            "duration_seconds": 2.0,
            "command": "python -m pytest tests",
            "return_code": 1,
            "stdout_tail": "failed",
            "stderr_tail": "",
            "started_at": "2026-01-01T00:00:00Z",
            "finished_at": "2026-01-01T00:00:02Z",
            "workspace_path": "/tmp/b",
            "test_count": 1,
            "error_summary": "failed",
        },
    ]

    leaderboard = build_leaderboard(payload)

    assert "PipelineBench Leaderboard" in leaderboard.markdown
    assert "| Pass rate | 50.0% |" in leaderboard.markdown
    assert leaderboard.summary["passed_tasks"] == 1


def test_cli_help_and_list_tasks() -> None:
    runner = CliRunner()

    help_result = runner.invoke(app, ["--help"])
    list_result = runner.invoke(app, ["list-tasks"])

    assert help_result.exit_code == 0
    assert "PipelineBench" in help_result.output
    assert list_result.exit_code == 0
    assert "broken_csv_ingestion" in list_result.output


def test_starter_task_validation_fails_before_fix(tmp_path: Path) -> None:
    task = load_task("broken_csv_ingestion")
    workspace = prepare_workspace(task, tmp_path / "broken_csv_ingestion")

    result = run_validation(task=task, workspace=workspace, command=task.validation_command)

    assert result.passed is False
    assert result.return_code != 0
